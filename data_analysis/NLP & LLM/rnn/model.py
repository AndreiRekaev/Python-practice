from typing import Dict, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import PackedSequence, pack_padded_sequence, pad_packed_sequence

from dataset import Vocab


def prepare_emb_matrix(gensim_model, vocab: Vocab, use_pretrained=True):
    """
    Улучшенная подготовка матрицы эмбеддингов с нормализацией
    """
    if not use_pretrained:
        return torch.randn(len(vocab), 300) * 0.1

    vec_size = gensim_model.vector_size
    emb_matrix = torch.zeros((len(vocab), vec_size))

    # Статистика для инициализации OOV слов
    all_vectors = []
    for word in vocab.itos[4:]:  # Пропускаем спецтокены
        try:
            vec = gensim_model.get_vector(word)
            all_vectors.append(vec)
        except KeyError:
            pass

    if all_vectors:
        all_vectors = torch.tensor(all_vectors)
        mean = all_vectors.mean(0)
        std = all_vectors.std(0)
    else:
        mean = torch.zeros(vec_size)
        std = torch.ones(vec_size) * 0.1

    for i, word in enumerate(vocab.itos):
        if i < 4:  # Спецтокены
            emb_matrix[i] = torch.randn(vec_size) * 0.01
            continue

        try:
            emb_matrix[i] = torch.tensor(gensim_model.get_vector(word))
        except KeyError:
            emb_matrix[i] = torch.randn(vec_size) * std + mean

    return emb_matrix


class Attention(nn.Module):
    """Механизм внимания для взвешенного суммирования скрытых состояний"""

    def __init__(self, hidden_size, bidirectional):
        super().__init__()
        self.hidden_size = hidden_size
        self.bidirectional = bidirectional
        self.attention = nn.Linear(hidden_size * (2 if bidirectional else 1), 1)

    def forward(self, outputs, lengths):
        # outputs: (batch, seq_len, hidden_size * (2 if bidirectional else 1))
        attention_weights = torch.tanh(self.attention(outputs))
        attention_weights = attention_weights.squeeze(-1)

        # Mask padding
        mask = torch.arange(outputs.size(1), device=outputs.device).unsqueeze(0) < lengths.unsqueeze(1)
        attention_weights = attention_weights.masked_fill(~mask, -1e9)

        attention_weights = F.softmax(attention_weights, dim=1)
        context = torch.bmm(attention_weights.unsqueeze(1), outputs).squeeze(1)
        return context, attention_weights


class RecurrentClassifier(nn.Module):
    def __init__(self, config: Dict, vocab: Vocab, emb_matrix):
        super().__init__()
        self.config = config
        self.vocab = vocab

        # Embeddings с dropout
        self.embeddings = nn.Embedding.from_pretrained(
            emb_matrix,
            freeze=config.get("freeze", False),
            padding_idx=vocab.PAD_IDX
        )
        self.emb_dropout = nn.Dropout(config.get("emb_dropout", 0.2))

        # Рекуррентный слой
        cell_types = {"RNN": nn.RNN, "GRU": nn.GRU, "LSTM": nn.LSTM}
        cell_class = cell_types[config["cell_type"]]

        self.cell = cell_class(
            input_size=emb_matrix.size(1),
            batch_first=True,
            hidden_size=config["hidden_size"],
            num_layers=config["num_layers"],
            dropout=config["cell_dropout"] if config["num_layers"] > 1 else 0,
            bidirectional=config["bidirectional"],
        )

        # Механизм внимания
        self.use_attention = config.get("use_attention", True)
        if self.use_attention:
            self.attention = Attention(config["hidden_size"], config["bidirectional"])

        # Выходной MLP
        self.out_dropout = nn.Dropout(config["out_dropout"])

        hidden_multiplier = 2 if config["bidirectional"] else 1
        input_size = config["hidden_size"] * hidden_multiplier

        # Batch Normalization между слоями
        out_layers = []
        for i, cur_hidden_size in enumerate(config["out_sizes"]):
            out_layers.append(nn.Linear(input_size, cur_hidden_size))
            out_layers.append(nn.BatchNorm1d(cur_hidden_size))
            out_layers.append(nn.ReLU())
            out_layers.append(nn.Dropout(config["out_dropout"]))
            input_size = cur_hidden_size

        out_layers.append(nn.Linear(input_size, 5))
        self.out_proj = nn.Sequential(*out_layers)

        # Весовая регуляризация
        self.apply(self._init_weights)

    def _init_weights(self, module):
        """Инициализация весов"""
        if isinstance(module, nn.Linear):
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.LSTM):
            for name, param in module.named_parameters():
                if 'weight_ih' in name:
                    nn.init.xavier_uniform_(param)
                elif 'weight_hh' in name:
                    nn.init.orthogonal_(param)
                elif 'bias' in name:
                    nn.init.zeros_(param)

    def forward(self, texts, lengths=None):
        # Embeddings
        embedded = self.embeddings(texts)
        embedded = self.emb_dropout(embedded)

        # Pack sequence для эффективности
        if lengths is not None:
            packed = pack_padded_sequence(embedded, lengths.cpu(), batch_first=True, enforce_sorted=False)
            outputs, hidden = self.cell(packed)
            outputs, _ = pad_packed_sequence(outputs, batch_first=True)
        else:
            outputs, hidden = self.cell(embedded)

        # Attention или последнее состояние
        if self.use_attention and lengths is not None:
            context, _ = self.attention(outputs, lengths)
        else:
            if isinstance(hidden, tuple):  # LSTM
                hidden = hidden[0]
            # Берём последний слой и направление
            if self.config["bidirectional"]:
                # Concatenate forward and backward last states
                hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
            else:
                hidden = hidden[-1]
            context = hidden

        # Классификация
        logits = self.out_proj(self.out_dropout(context))
        return logits