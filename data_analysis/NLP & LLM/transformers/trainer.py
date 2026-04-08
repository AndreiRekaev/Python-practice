"""
Оптимизированный тренер с поддержкой:
- Mixed precision (FP16)
- Gradient accumulation
- Early stopping
- Cosine annealing scheduler
- Поддержка кастомных моделей
"""

from typing import Dict
import numpy as np
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.cuda.amp import autocast, GradScaler
import torch.nn.functional as F
from transformers import get_linear_schedule_with_warmup, get_cosine_schedule_with_warmup
from tqdm.notebook import tqdm

from sklearn.metrics import f1_score, accuracy_score


class EarlyStopping:
    def __init__(self, patience=3, min_delta=1e-4):
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
                model.load_state_dict(self.best_model_state)
                return True
            return False


class Trainer:
    def __init__(self, config: Dict):
        self.config = config
        self.n_epochs = config['n_epochs']
        self.device = config['device']
        self.verbose = config.get('verbose', True)

        # Mixed precision
        self.use_amp = config.get('use_amp', False) and self.device == 'cuda'
        self.scaler = GradScaler() if self.use_amp else None

        # Gradient accumulation
        self.grad_accum_steps = config.get('grad_accum_steps', 1)

        # Loss function
        loss_type = config.get('loss_type', 'cross_entropy')
        if loss_type == 'focal':
            self.loss_fn = FocalLoss(alpha=1, gamma=2)
        else:
            self.loss_fn = nn.CrossEntropyLoss(label_smoothing=config.get('label_smoothing', 0.05))

        self.model = None
        self.optimizer = None
        self.scheduler = None
        self.history = None
        self.early_stopping = EarlyStopping(patience=config.get('patience', 3))

    def fit(self, model, train_dataloader, val_dataloader):
        self.model = model.to(self.device)

        # Optimizer
        self.optimizer = AdamW(
            self.model.parameters(),
            lr=self.config['lr'],
            weight_decay=self.config.get('weight_decay', 1e-4),
            betas=(0.9, 0.999)
        )

        # Scheduler
        total_steps = len(train_dataloader) * self.n_epochs // self.grad_accum_steps
        warmup_steps = int(total_steps * self.config.get('warmup_ratio', 0.1))

        scheduler_type = self.config.get('scheduler', 'linear')
        if scheduler_type == 'cosine':
            self.scheduler = get_cosine_schedule_with_warmup(
                self.optimizer,
                num_warmup_steps=warmup_steps,
                num_training_steps=total_steps
            )
        else:
            self.scheduler = get_linear_schedule_with_warmup(
                self.optimizer,
                num_warmup_steps=warmup_steps,
                num_training_steps=total_steps
            )

        self.history = {
            'train_loss': [],
            'train_acc': [],
            'train_f1': [],
            'val_loss': [],
            'val_acc': [],
            'val_f1': [],
            'lr': []
        }

        best_val_f1 = 0

        for epoch in range(self.n_epochs):
            if self.verbose:
                print(f"\n{'=' * 50}")
                print(f"Эпоха {epoch + 1}/{self.n_epochs}")
                print(f"LR: {self.scheduler.get_last_lr()[0]:.2e}")

            # Training
            train_loss, train_acc, train_f1 = self._train_epoch(train_dataloader)

            # Validation
            val_loss, val_acc, val_f1 = self._val_epoch(val_dataloader)

            # History
            self.history['train_loss'].append(train_loss)
            self.history['train_acc'].append(train_acc)
            self.history['train_f1'].append(train_f1)
            self.history['val_loss'].append(val_loss)
            self.history['val_acc'].append(val_acc)
            self.history['val_f1'].append(val_f1)
            self.history['lr'].append(self.scheduler.get_last_lr()[0])

            if self.verbose:
                print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | Train F1: {train_f1:.4f}")
                print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f} | Val F1: {val_f1:.4f}")

            # Save best
            if val_f1 > best_val_f1:
                best_val_f1 = val_f1
                self.best_model_state = {k: v.cpu().clone() for k, v in self.model.state_dict().items()}
                if self.verbose:
                    print(f"✓ Новая лучшая модель! F1: {best_val_f1:.4f}")

            # Early stopping
            if self.early_stopping.check(val_f1, self.model):
                if self.verbose:
                    print(f"\nРанняя остановка на эпохе {epoch + 1}. Лучший F1: {best_val_f1:.4f}")
                break

        # Restore best model
        if hasattr(self, 'best_model_state'):
            self.model.load_state_dict(self.best_model_state)

        if self.verbose:
            print(f"\n{'=' * 50}")
            print(f"Лучший F1: {best_val_f1:.4f}")

        return self.model.eval()

    def _train_epoch(self, dataloader):
        self.model.train()
        total_loss = 0
        all_preds = []
        all_labels = []

        if self.verbose:
            dataloader = tqdm(dataloader, desc="Обучение")

        self.optimizer.zero_grad()

        for step, batch in enumerate(dataloader):
            # Распаковка батча
            if len(batch) == 3:
                input_ids, attention_mask, labels = batch
            else:
                input_ids, attention_mask = batch
                labels = None

            input_ids = input_ids.to(self.device)
            attention_mask = attention_mask.to(self.device)
            if labels is not None:
                labels = labels.to(self.device)

            # Forward
            if self.use_amp:
                with autocast():
                    logits = self.model(input_ids, attention_mask)
                    loss = self.loss_fn(logits, labels) if labels is not None else logits
            else:
                logits = self.model(input_ids, attention_mask)
                loss = self.loss_fn(logits, labels) if labels is not None else logits

            # Backward
            if self.use_amp:
                self.scaler.scale(loss).backward()
            else:
                loss.backward()

            # Gradient accumulation
            if (step + 1) % self.grad_accum_steps == 0:
                if self.use_amp:
                    self.scaler.unscale_(self.optimizer)
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                    self.scaler.step(self.optimizer)
                    self.scaler.update()
                else:
                    torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                    self.optimizer.step()

                self.scheduler.step()
                self.optimizer.zero_grad()

            total_loss += loss.item()

            if labels is not None:
                preds = logits.argmax(1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

                if self.verbose:
                    current_acc = accuracy_score(all_labels, all_preds)
                    dataloader.set_postfix(loss=loss.item(), acc=current_acc)

        avg_loss = total_loss / len(dataloader)
        avg_acc = accuracy_score(all_labels, all_preds) if all_labels else 0
        avg_f1 = f1_score(all_labels, all_preds, average='weighted') if all_labels else 0

        return avg_loss, avg_acc, avg_f1

    def _val_epoch(self, dataloader):
        self.model.eval()
        total_loss = 0
        all_preds = []
        all_labels = []

        if self.verbose:
            dataloader = tqdm(dataloader, desc="Валидация")

        with torch.no_grad():
            for batch in dataloader:
                if len(batch) == 3:
                    input_ids, attention_mask, labels = batch
                else:
                    input_ids, attention_mask = batch
                    labels = None

                input_ids = input_ids.to(self.device)
                attention_mask = attention_mask.to(self.device)
                if labels is not None:
                    labels = labels.to(self.device)

                if self.use_amp:
                    with autocast():
                        logits = self.model(input_ids, attention_mask)
                        loss = self.loss_fn(logits, labels) if labels is not None else logits
                else:
                    logits = self.model(input_ids, attention_mask)
                    loss = self.loss_fn(logits, labels) if labels is not None else logits

                total_loss += loss.item()

                if labels is not None:
                    preds = logits.argmax(1)
                    all_preds.extend(preds.cpu().numpy())
                    all_labels.extend(labels.cpu().numpy())

        avg_loss = total_loss / len(dataloader)
        avg_acc = accuracy_score(all_labels, all_preds) if all_labels else 0
        avg_f1 = f1_score(all_labels, all_preds, average='weighted') if all_labels else 0

        return avg_loss, avg_acc, avg_f1

    def predict(self, dataloader):
        if self.model is None:
            raise RuntimeError("Сначала обучите модель!")

        self.model.eval()
        predictions = []

        with torch.no_grad():
            for batch in tqdm(dataloader, desc="Предсказание"):
                if len(batch) == 3:
                    input_ids, attention_mask, _ = batch
                else:
                    input_ids, attention_mask = batch

                input_ids = input_ids.to(self.device)
                attention_mask = attention_mask.to(self.device)

                if self.use_amp:
                    with autocast():
                        logits = self.model(input_ids, attention_mask)
                else:
                    logits = self.model(input_ids, attention_mask)

                predictions.extend(logits.argmax(1).cpu().numpy())

        return np.array(predictions)

    def save(self, path: str):
        if self.model is None:
            raise RuntimeError("Сначала обучите модель!")

        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'config': self.config,
            'history': self.history
        }
        torch.save(checkpoint, path)
        if self.verbose:
            print(f"Модель сохранена в {path}")

    def load(self, path: str, model):
        checkpoint = torch.load(path, map_location=self.device)
        model.load_state_dict(checkpoint['model_state_dict'])
        self.model = model.to(self.device)
        self.history = checkpoint.get('history', {})
        if self.verbose:
            print(f"Модель загружена из {path}")
        return self.model


class FocalLoss(nn.Module):
    """Focal Loss для фокусировки на сложных примерах"""

    def __init__(self, alpha=1, gamma=2, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * ce_loss

        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss