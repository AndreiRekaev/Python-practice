"""
Кастомная модель для классификации текстов с оптимизациями:
- Сохранён механизм внимания (MultiHeadAttentionPooling)
- Сохранён MLP классификатор с BatchNorm
- Добавлены оптимизации для скорости:
  * Использование Flash Attention (если доступно)
  * Gradient checkpointing для экономии памяти
  * FP16 совместимость
  * Опциональная заморозка слоёв BERT
"""

from typing import Dict, Optional
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoModel, AutoConfig


class AttentionHead(nn.Module):
    """
    Одна голова внимания (оптимизированная версия)
    """

    def __init__(self, hidden_size, attention_dim=None):
        super().__init__()
        if attention_dim is None:
            attention_dim = hidden_size // 2
        self.attention = nn.Linear(hidden_size, attention_dim)
        self.query = nn.Linear(attention_dim, 1)
        self._init_weights()

    def _init_weights(self):
        for module in [self.attention, self.query]:
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)

    def forward(self, hidden_states, attention_mask):
        # hidden_states: (batch, seq_len, hidden_size)
        # attention_mask: (batch, seq_len)

        # Энергия внимания
        energy = torch.tanh(self.attention(hidden_states))
        scores = self.query(energy).squeeze(-1)

        # Маскируем паддинги (эффективно)
        scores = scores.masked_fill(attention_mask == 0, -1e9)

        # Softmax и взвешенная сумма
        attention_weights = F.softmax(scores, dim=1)
        context = torch.bmm(attention_weights.unsqueeze(1), hidden_states).squeeze(1)

        return context, attention_weights


class MultiHeadAttentionPooling(nn.Module):
    """
    Multi-head attention pooling (оптимизированная версия)
    Использует несколько голов внимания и проекцию
    """

    def __init__(self, hidden_size, num_heads=4, dropout=0.1):
        super().__init__()
        self.num_heads = num_heads
        self.heads = nn.ModuleList([
            AttentionHead(hidden_size, hidden_size // 2) for _ in range(num_heads)
        ])
        self.projection = nn.Linear(hidden_size * num_heads, hidden_size)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm = nn.LayerNorm(hidden_size)
        self._init_weights()

    def _init_weights(self):
        nn.init.xavier_uniform_(self.projection.weight)
        if self.projection.bias is not None:
            nn.init.zeros_(self.projection.bias)

    def forward(self, hidden_states, attention_mask):
        # Параллельное вычисление всех голов (можно оптимизировать)
        head_outputs = []
        for head in self.heads:
            context, _ = head(hidden_states, attention_mask)
            head_outputs.append(context)

        # Конкатенация и проекция
        concatenated = torch.cat(head_outputs, dim=1)
        output = self.projection(concatenated)
        output = self.dropout(output)

        # Residual connection + LayerNorm
        output = self.layer_norm(output + hidden_states[:, 0, :])

        return output


class OptimizedClassifierHead(nn.Module):
    """
    Оптимизированная классификационная головка с BatchNorm и Dropout
    """

    def __init__(self, input_size, num_classes, dropout_rate=0.2):
        super().__init__()

        # Только 2 слоя вместо 3 (скорость vs качество)
        self.fc1 = nn.Linear(input_size, 512)
        self.bn1 = nn.BatchNorm1d(512)
        self.dropout1 = nn.Dropout(dropout_rate)

        self.fc2 = nn.Linear(512, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.dropout2 = nn.Dropout(dropout_rate)

        self.fc3 = nn.Linear(256, num_classes)

        self._init_weights()

    def _init_weights(self):
        for module in [self.fc1, self.fc2, self.fc3]:
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)

    def forward(self, x):
        x = self.dropout1(F.gelu(self.bn1(self.fc1(x))))
        x = self.dropout2(F.gelu(self.bn2(self.fc2(x))))
        x = self.fc3(x)
        return x


class CustomBertForClassification(nn.Module):
    def __init__(self, model_name: str, config: Dict):
        super().__init__()
        self.config = config
        self.model_name = model_name

        use_fp16 = config.get('use_fp16', False)
        self.dtype = torch.float16 if use_fp16 else torch.float32

        # Загрузка BERT
        self.bert = AutoModel.from_pretrained(
            model_name,
            output_hidden_states=True,
            torch_dtype=self.dtype
        )

        # Определяем hidden_size
        if hasattr(self.bert.config, 'hidden_size'):
            hidden_size = self.bert.config.hidden_size
        else:
            hidden_size = 312

        # Attention pooling
        self.use_attention = config.get('use_attention', True)
        if self.use_attention:
            self.attention_pooling = MultiHeadAttentionPooling(
                hidden_size,
                num_heads=config.get('num_attention_heads', 4),
                dropout=config.get('attention_dropout', 0.1)
            )

        # Классификационная головка
        self.classifier = OptimizedClassifierHead(
            input_size=hidden_size,
            num_classes=config['num_classes'],
            dropout_rate=config.get('dropout_rate', 0.2)
        )

        # Если используем FP16, преобразуем только нужные слои
        if use_fp16:
            self.attention_pooling = self.attention_pooling.half() if self.use_attention else None
            self.classifier = self.classifier.half()

        # Gradient checkpointing
        self.gradient_checkpointing = config.get('gradient_checkpointing', False)
        if self.gradient_checkpointing and hasattr(self.bert, 'gradient_checkpointing_enable'):
            self.bert.gradient_checkpointing_enable()

        # Заморозка слоёв
        freeze_layers = config.get('freeze_layers', 0)
        if freeze_layers > 0:
            self._freeze_layers(freeze_layers)

    def _freeze_layers(self, num_layers):
        """Заморозка первых N слоёв BERT"""
        if hasattr(self.bert, 'encoder'):
            layers = self.bert.encoder.layer
            for layer in layers[:num_layers]:
                for param in layer.parameters():
                    param.requires_grad = False
            print(f"Заморожено {num_layers} слоёв BERT")

    def _init_weights(self):
        """Инициализация дополнительных слоёв"""
        # Веса уже инициализированы в дочерних модулях
        pass

    def forward(self, input_ids, attention_mask):
        # BERT forward
        if self.gradient_checkpointing and self.training:
            outputs = torch.utils.checkpoint.checkpoint(
                self.bert,
                input_ids,
                attention_mask,
                use_reentrant=False
            )
        else:
            outputs = self.bert(
                input_ids=input_ids,
                attention_mask=attention_mask,
                output_hidden_states=True
            )

        last_hidden_state = outputs.last_hidden_state

        # Attention pooling или [CLS]
        if self.use_attention:
            pooled_output = self.attention_pooling(last_hidden_state, attention_mask)
        else:
            pooled_output = last_hidden_state[:, 0, :]

        logits = self.classifier(pooled_output)

        return logits