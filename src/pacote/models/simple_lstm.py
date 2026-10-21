from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from torch import nn


@dataclass
class SequenceDataset:
    """Estrutura simples para sequências de entrada e alvos."""

    X: np.ndarray
    y: np.ndarray


class SimpleLSTMRegressor:
    """Regressor LSTM mínimo para séries temporais univariadas."""

    def __init__(self, input_size: int = 1, hidden_size: int = 8, seq_len: int = 16, lr: float = 1e-2):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.seq_len = seq_len
        self.lr = lr
        self.model = nn.Sequential(
            nn.LSTM(input_size=input_size, hidden_size=hidden_size, batch_first=True),
            nn.Linear(hidden_size, 1),
        )
        self.loss_fn = nn.MSELoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)

    def _prepare_sequences(self, X: np.ndarray, y: np.ndarray):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.shape[0] != y.shape[0]:
            raise ValueError("X e y precisam ter o mesmo tamanho")
        n_samples = X.shape[0] - self.seq_len + 1
        if n_samples <= 0:
            raise ValueError("seq_len excede o tamanho dos dados")

        windows = np.stack([X[i : i + self.seq_len] for i in range(n_samples)])
        targets = y[self.seq_len - 1 : self.seq_len - 1 + n_samples]
        return windows, targets

    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 25):
        windows, targets = self._prepare_sequences(X, y)
        X_t = torch.tensor(windows, dtype=torch.float32)
        y_t = torch.tensor(targets, dtype=torch.float32).reshape(-1, 1)

        for _ in range(epochs):
            self.optimizer.zero_grad()
            pred = self.model(X_t)[-1]
            loss = self.loss_fn(pred, y_t)
            loss.backward()
            self.optimizer.step()

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=float)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        if X.shape[0] < self.seq_len:
            raise ValueError("dados insuficientes para a janela de previsão")

        window = X[-self.seq_len :].reshape(1, self.seq_len, self.input_size)
        with torch.no_grad():
            pred = self.model(torch.tensor(window, dtype=torch.float32))[-1]
        return pred.detach().numpy().reshape(-1)
