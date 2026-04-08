import re
import torch
import numpy as np
from torch.utils.data import Dataset
from sklearn.utils.class_weight import compute_class_weight


def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower().strip()
    return text


class FiveDataset(Dataset):
    """
    Оптимизированный датасет для трансформеров с кэшированием токенов
    """

    def __init__(self, dataframe, tokenizer, max_seq_len, cache_tokens=False):
        """
        :param dataframe: pandas DataFrame с колонками text и rate
        :param tokenizer: токенизатор HuggingFace
        :param max_seq_len: максимальная длина последовательности
        :param cache_tokens: кэшировать ли токены (ускоряет, но требует больше RAM)
        """
        self.data = dataframe.reset_index(drop=True)
        self.tokenizer = tokenizer
        self.max_seq_len = max_seq_len

        # Очищаем тексты
        self.texts = [clean_text(str(t)) for t in self.data['text'].tolist()]

        # Метки
        self.targets = None
        if 'rate' in dataframe.columns:
            self.targets = self.data['rate'].tolist()

        # Кэш для токенов
        self.cache_tokens = cache_tokens
        self.input_ids_cache = None
        self.attention_mask_cache = None

        if cache_tokens:
            self._precompute_tokens()

    def _precompute_tokens(self):
        """
        Предварительное вычисление всех токенов (ускоряет обучение, но требует больше памяти)
        """
        print("Предварительное кэширование токенов...")
        self.input_ids_cache = []
        self.attention_mask_cache = []

        for text in self.texts:
            inputs = self.tokenizer(
                text,
                max_length=self.max_seq_len,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            self.input_ids_cache.append(inputs['input_ids'].squeeze(0))
            self.attention_mask_cache.append(inputs['attention_mask'].squeeze(0))

        print(f"Кэширование завершено. Объём: {len(self.input_ids_cache)} образцов")

    def __getitem__(self, index):
        # Берём из кэша или токенизируем на лету
        if self.cache_tokens:
            ids = self.input_ids_cache[index]
            mask = self.attention_mask_cache[index]
        else:
            text = self.texts[index]
            inputs = self.tokenizer(
                text,
                max_length=self.max_seq_len,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            ids = inputs['input_ids'].squeeze(0)
            mask = inputs['attention_mask'].squeeze(0)

        if self.targets is not None:
            return {
                'input_ids': ids,
                'attention_mask': mask,
                'labels': torch.tensor(self.targets[index], dtype=torch.long)
            }
        else:
            return {
                'input_ids': ids,
                'attention_mask': mask,
            }

    def __len__(self):
        return len(self.texts)

    @staticmethod
    def collate_fn(batch):
        """
        Эффективная функция для батча
        """
        input_ids = torch.stack([item['input_ids'] for item in batch])
        attention_mask = torch.stack([item['attention_mask'] for item in batch])

        if 'labels' in batch[0]:
            labels = torch.stack([item['labels'] for item in batch])
            return input_ids, attention_mask, labels
        return input_ids, attention_mask


def create_dataloaders(train_data, val_data, test_data, tokenizer, config):
    """
    Утилита для создания всех dataloaders с оптимальными параметрами
    """
    from torch.utils.data import DataLoader

    train_dataset = FiveDataset(
        train_data,
        tokenizer,
        config['max_len'],
        cache_tokens=config.get('cache_tokens', False)
    )

    val_dataset = FiveDataset(
        val_data,
        tokenizer,
        config['max_len'],
        cache_tokens=config.get('cache_tokens', False)
    )

    test_dataset = FiveDataset(
        test_data,
        tokenizer,
        config['max_len'],
        cache_tokens=config.get('cache_tokens', False)
    )

    loader_params = {
        'batch_size': config['batch_size'],
        'num_workers': config.get('num_workers', 4),
        'pin_memory': config.get('pin_memory', True),
        'persistent_workers': config.get('num_workers', 0) > 0,
        'prefetch_factor': config.get('prefetch_factor', 2)
    }

    train_loader = DataLoader(
        train_dataset,
        shuffle=True,
        collate_fn=FiveDataset.collate_fn,
        **loader_params
    )

    val_loader = DataLoader(
        val_dataset,
        shuffle=False,
        collate_fn=FiveDataset.collate_fn,
        **loader_params
    )

    test_loader = DataLoader(
        test_dataset,
        shuffle=False,
        collate_fn=FiveDataset.collate_fn,
        **loader_params
    )

    return train_loader, val_loader, test_loader