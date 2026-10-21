from __future__ import annotations

import numpy as np
import torch
from torch import nn


class LSTMRegressor:
    """Regressor LSTM simples para séries temporais univariadas."""

    def __init__(
        self,
        input_size: int = 1,
        hidden_size: int = 8,
        num_layers: int = 1,
        learning_rate: float = 1e-3,
        device: str | None = None,
    ) -> None:
        self.device = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        self.model = nn.Sequential(
            nn.LSTM(
                input_size=input_size,
                hidden_size=hidden_size,
                num_layers=num_layers,
                batch_first=True,
            ),
            nn.Linear(hidden_size, 1),
        ).to(self.device)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()

    def _prepare_inputs(self, X: np.ndarray, y: np.ndarray | None = None):
        X_tensor = torch.tensor(np.asarray(X, dtype=np.float32), device=self.device)
        X_tensor = X_tensor.reshape(X_tensor.shape[0], -1, 1)
        if y is None:
            return X_tensor
        y_tensor = torch.tensor(np.asarray(y, dtype=np.float32), device=self.device)
        y_tensor = y_tensor.reshape(y_tensor.shape[0], -1, 1)
        return X_tensor, y_tensor

    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 10, batch_size: int = 32) -> None:
        X_tensor, y_tensor = self._prepare_inputs(X, y)
        for _ in range(epochs):
            for start in range(0, len(X_tensor), batch_size):
                xb = X_tensor[start : start + batch_size]
                yb = y_tensor[start : start + batch_size]

                self.optimizer.zero_grad()
                pred, _ = self.model[0](xb)
                pred = self.model[1](pred)
                loss = self.loss_fn(pred, yb)
                loss.backward()
                self.optimizer.step()

    def predict(self, X: np.ndarray) -> np.ndarray:
        X_tensor = self._prepare_inputs(X)
        self.model.eval()
        with torch.no_grad():
            pred, _ = self.model[0](X_tensor)
            pred = self.model[1](pred)
            return pred.cpu().numpy().reshape(-1, 1)
