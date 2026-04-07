import re
from collections import Counter
from itertools import chain
from typing import List, Optional
import numpy as np

import torch
from torch.nn.utils.rnn import pack_sequence, pad_sequence
from torch.utils.data import Dataset, DataLoader


class Tokenizer:
    """Продвинутый токенизатор с поддержкой стоп-слов и стемминга"""

    def __init__(self, use_stopwords=True, use_stemming=False):
        self.word_pattern = re.compile(r'[а-яёa-z]+(?:-[а-яёa-z]+)?')
        self.use_stopwords = use_stopwords
        self.use_stemming = use_stemming

        # Русские стоп-слова (можно расширить)
        self.stop_words = {
            'и', 'в', 'во', 'не', 'что', 'на', 'я', 'с', 'со', 'как', 'а',
            'но', 'он', 'по', 'у', 'же', 'из', 'за', 'то', 'так', 'же',
            'вы', 'весь', 'это', 'все', 'о', 'при', 'к', 'очень', 'было',
            'только', 'еще', 'уже', 'вот', 'бы', 'да', 'нет', 'для', 'до',
            'или', 'без', 'через', 'над', 'под', 'об', 'про', 'этот', 'тот'
        }

        # Простой стеммер для русского языка
        self.suffixes = {
            'ую', 'юю', 'ая', 'яя', 'ое', 'ее', 'ые', 'ие', 'ой', 'ей',
            'ый', 'ий', 'ого', 'его', 'ому', 'ему', 'ым', 'им', 'ом', 'ем',
            'ать', 'ять', 'ить', 'еть', 'уть', 'ют', 'ит', 'ет', 'ат', 'ят'
        }

    def tokenize(self, text: str) -> List[str]:
        """Токенизация с очисткой"""
        if not isinstance(text, str):
            return []

        # Приводим к нижнему регистру
        text = text.lower()
        # Находим все слова
        tokens = self.word_pattern.findall(text)

        # Удаляем короткие слова (меньше 2 букв)
        tokens = [t for t in tokens if len(t) >= 2]

        # Удаляем стоп-слова
        if self.use_stopwords:
            tokens = [t for t in tokens if t not in self.stop_words]

        # Стемминг (упрощённый)
        if self.use_stemming:
            tokens = [self._stem(t) for t in tokens]

        return tokens

    def _stem(self, word: str) -> str:
        """Простой суффиксный стеммер"""
        for suffix in self.suffixes:
            if word.endswith(suffix):
                word = word[:-len(suffix)]
                break
        return word


class Vocab:
    def __init__(self, tokenized_texts: List[List[str]], max_vocab_size=None, min_freq=2):
        """
        Словарь с поддержкой минимальной частоты и предобученных эмбеддингов
        """
        # Подсчёт частот
        counts = Counter(chain(*tokenized_texts))

        # Фильтрация по минимальной частоте
        if min_freq > 1:
            counts = {word: cnt for word, cnt in counts.items() if cnt >= min_freq}

        max_vocab_size = max_vocab_size or len(counts)

        # Берём самые частотные слова
        common_pairs = Counter(counts).most_common(max_vocab_size)

        # Специальные токены
        self.PAD_IDX = 0
        self.UNK_IDX = 1
        self.EOS_IDX = 2
        self.SOS_IDX = 3  # Начало предложения (для encoder-decoder)

        self.itos = ["<PAD>", "<UNK>", "<EOS>", "<SOS>"] + [pair[0] for pair in common_pairs]
        self.stoi = {token: i for i, token in enumerate(self.itos)}

        # Словарь для быстрого поиска частот
        self.word_freq = counts

    def vectorize(self, text: List[str], add_sos=False):
        """
        Векторизация с опциональным добавлением токена начала
        """
        tokens = [self.stoi.get(tok, self.UNK_IDX) for tok in text]
        if add_sos:
            tokens = [self.SOS_IDX] + tokens
        tokens.append(self.EOS_IDX)
        return tokens

    def __len__(self):
        return len(self.itos)


class TextDataset(Dataset):
    def __init__(self, tokenized_texts, labels, vocab, max_seq_len=None):
        """
        Датасет с паддингом до максимальной длины
        """
        self.texts = tokenized_texts
        self.labels = labels
        self.vocab = vocab
        self.max_seq_len = max_seq_len or self._get_max_len(tokenized_texts)

    def _get_max_len(self, texts):
        """Вычисление 95-го перцентиля длин текстов"""
        lengths = [len(t) for t in texts]
        return int(np.percentile(lengths, 95))

    def __getitem__(self, item):
        vectorized = self.vocab.vectorize(self.texts[item])

        # Обрезаем слишком длинные тексты
        if len(vectorized) > self.max_seq_len:
            vectorized = vectorized[:self.max_seq_len - 1] + [self.vocab.EOS_IDX]

        return (
            torch.tensor(vectorized, dtype=torch.long),
            torch.tensor(self.labels[item], dtype=torch.long)
        )

    def __len__(self):
        return len(self.texts)

    def collate_fn(self, batch):
        """Кастомная функция для паддинга"""
        texts, labels = zip(*batch)

        # Паддинг до максимальной длины в батче
        padded_texts = pad_sequence(texts, batch_first=True, padding_value=self.vocab.PAD_IDX)
        labels = torch.tensor(labels, dtype=torch.long)

        # Длины последовательностей для pack_padded_sequence
        lengths = torch.tensor([len(t) for t in texts], dtype=torch.long)

        return padded_texts, labels, lengths


def train_test_split(data, train_frac=0.85, random_state=42):
    """
    Стратифицированное разделение с перемешиванием
    """
    np.random.seed(random_state)
    n_toxicity_ratings = 5
    train_labels = []
    val_labels = []
    train_texts = []
    val_texts = []

    for label in range(n_toxicity_ratings):
        texts = data[data.rate == label].text.values
        # Перемешиваем
        indices = np.random.permutation(len(texts))
        texts = texts[indices]

        n_train = int(len(texts) * train_frac)
        train_texts.extend(texts[:n_train])
        val_texts.extend(texts[n_train:])
        train_labels += [label] * n_train
        val_labels += [label] * (len(texts) - n_train)

    return train_texts, train_labels, val_texts, val_labels