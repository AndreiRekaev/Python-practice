from typing import Dict
import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam, AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau, CosineAnnealingWarmRestarts
from tqdm.notebook import tqdm
from sklearn.metrics import f1_score

from model import RecurrentClassifier


class EarlyStopping:
    """Ранняя остановка с восстановлением лучших весов"""

    def __init__(self, patience=5, min_delta=1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_score = None
        self.best_model_state = None

    def check(self, score, model):
        if self.best_score is None or score > self.best_score + self.min_delta:
            self.best_score = score
            self.best_model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            self.counter = 0
            return False
        else:
            self.counter += 1
            if self.counter >= self.patience:
                # Восстанавливаем лучшие веса
                model.load_state_dict(self.best_model_state)
                return True
            return False


class Trainer:
    def __init__(self, config: Dict):
        self.config = config
        self.n_epochs = config["n_epochs"]

        # Используем AdamW (лучше чем Adam)
        self.setup_opt_fn = lambda model: AdamW(
            model.parameters(),
            lr=config["lr"],
            weight_decay=config["weight_decay"],
            betas=(0.9, 0.999)
        )

        self.model = None
        self.opt = None
        self.scheduler = None
        self.history = None
        self.loss_fn = nn.CrossEntropyLoss(label_smoothing=0.1)  # Label smoothing
        self.device = config["device"]
        self.verbose = config.get("verbose", True)

        # Ранняя остановка
        self.early_stopping = EarlyStopping(patience=config.get("patience", 5))

    def fit(self, model, train_loader, val_loader):
        self.model = model.to(self.device)
        self.opt = self.setup_opt_fn(self.model)

        # Cosine annealing with warm restarts
        self.scheduler = CosineAnnealingWarmRestarts(
            self.opt,
            T_0=len(train_loader),
            T_mult=2,
            eta_min=1e-6
        )

        self.history = {
            "train_loss": [],
            "train_acc": [],
            "val_loss": [],
            "val_acc": [],
            "val_f1": []
        }

        best_val_f1 = 0

        for epoch in range(self.n_epochs):
            print(f"\n{'=' * 50}")
            print(f"Эпоха {epoch + 1}/{self.n_epochs}")
            print(f"LR: {self.scheduler.get_last_lr()[0]:.6f}")

            # Обучение
            train_loss, train_acc = self._train_epoch(train_loader)

            # Валидация
            val_loss, val_acc, val_f1 = self._val_epoch(val_loader)

            # Сохраняем историю
            self.history["train_loss"].append(train_loss)
            self.history["train_acc"].append(train_acc)
            self.history["val_loss"].append(val_loss)
            self.history["val_acc"].append(val_acc)
            self.history["val_f1"].append(val_f1)

            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}, Val F1: {val_f1:.4f}")

            # Сохраняем лучшую модель по F1
            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                self.best_model_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}
                print(f"✓ Новая лучшая модель! F1: {best_val_f1:.4f}")

            # Ранняя остановка
            if self.early_stopping.check(val_f1, self.model):
                print(f"\nРанняя остановка на эпохе {epoch + 1}. Лучший F1: {best_val_f1:.4f}")
                break

        # Восстанавливаем лучшую модель
        if hasattr(self, 'best_model_state'):
            self.model.load_state_dict(self.best_model_state)

        print(f"\n{'=' * 50}")
        print(f"Лучший F1 на валидации: {best_val_f1:.4f}")

        return self.model.eval()

    def _train_epoch(self, train_loader):
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0

        if self.verbose:
            train_loader = tqdm(train_loader, desc="Обучение")

        for batch in train_loader:
            self.opt.zero_grad()

            # Распаковываем батч
            if len(batch) == 3:
                texts, labels, lengths = batch
                texts, labels, lengths = texts.to(self.device), labels.to(self.device), lengths.to(self.device)
                logits = self.model(texts, lengths)
            else:
                texts, labels = batch
                texts, labels = texts.to(self.device), labels.to(self.device)
                logits = self.model(texts)

            loss = self.loss_fn(logits, labels)
            loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)

            self.opt.step()
            self.scheduler.step()

            total_loss += loss.item()
            preds = logits.argmax(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

            if self.verbose:
                train_loader.set_postfix(loss=loss.item(), acc=correct / total)

        return total_loss / len(train_loader), correct / total

    def _val_epoch(self, val_loader):
        self.model.eval()
        total_loss = 0
        all_preds = []
        all_labels = []

        if self.verbose:
            val_loader = tqdm(val_loader, desc="Валидация")

        with torch.no_grad():
            for batch in val_loader:
                if len(batch) == 3:
                    texts, labels, lengths = batch
                    texts, labels, lengths = texts.to(self.device), labels.to(self.device), lengths.to(self.device)
                    logits = self.model(texts, lengths)
                else:
                    texts, labels = batch
                    texts, labels = texts.to(self.device), labels.to(self.device)
                    logits = self.model(texts)

                loss = self.loss_fn(logits, labels)
                total_loss += loss.item()

                preds = logits.argmax(1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

        accuracy = (np.array(all_preds) == np.array(all_labels)).mean()
        f1 = f1_score(all_labels, all_preds, average='weighted')

        return total_loss / len(val_loader), accuracy, f1

    def predict(self, test_loader):
        if self.model is None:
            raise RuntimeError("Сначала обучите модель!")

        self.model.eval()
        predictions = []

        with torch.no_grad():
            for batch in tqdm(test_loader, desc="Предсказание"):
                if len(batch) == 3:
                    texts, _, lengths = batch
                    texts, lengths = texts.to(self.device), lengths.to(self.device)
                    logits = self.model(texts, lengths)
                else:
                    texts, _ = batch
                    texts = texts.to(self.device)
                    logits = self.model(texts)

                predictions.extend(logits.argmax(1).cpu().numpy())

        return np.array(predictions)

    def save(self, path: str):
        if self.model is None:
            raise RuntimeError("Сначала обучите модель!")

        checkpoint = {
            "config": self.model.config,
            "trainer_config": self.config,
            "vocab": self.model.vocab,
            "state_dict": self.model.state_dict(),
            "history": self.history,
        }
        torch.save(checkpoint, path)
        print(f"Модель сохранена в {path}")

    @classmethod
    def load(cls, path: str):
        ckpt = torch.load(path, map_location='cpu')
        new_model = RecurrentClassifier(ckpt["config"], ckpt["vocab"], None)
        new_model.load_state_dict(ckpt["state_dict"])
        new_trainer = cls(ckpt["trainer_config"])
        new_trainer.model = new_model
        new_trainer.history = ckpt.get("history", {})
        return new_trainer