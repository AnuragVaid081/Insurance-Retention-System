from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from tensorflow.keras.preprocessing.sequence import pad_sequences

from training_features import MODEL_FEATURES
from preprocessing.tabular_preprocessing import fit_preprocessor


# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

DATASET = (
    ROOT
    / "Synthetic Generator"
    / "data"
    / "model_dataset.csv"
)

OUTPUT = ROOT / "saved_models"
OUTPUT.mkdir(exist_ok=True)

TARGET = "Renewed"

# ==========================================================
# Load Dataset
# ==========================================================

print("Loading dataset...")

df = pd.read_csv(DATASET)

print(df.shape)

# ==========================================================
# Preprocess
# ==========================================================

print("Preprocessing...")

df = fit_preprocessor(df)

print("Done preprocessing.")

# ==========================================================
# Sort by policy history
# ==========================================================

df = df.sort_values(
    ["Policy_Number", "Policy_Tenure"]
)

# ==========================================================
# Build Sequences
# ==========================================================

X_sequences = []
y = []

MIN_HISTORY = 2

print("Building sliding window sequences...")

for policy_number, history in df.groupby("Policy_Number"):

    history = history.sort_values("Policy_Tenure")

    if len(history) <= MIN_HISTORY:
        continue

    history_features = history[MODEL_FEATURES].values

    history_labels = history[TARGET].values

    for end in range(MIN_HISTORY, len(history)):

        sequence = history_features[:end]

        label = history_labels[end]

        X_sequences.append(sequence)

        y.append(label)

print()

print(f"Generated {len(X_sequences)} training sequences.")

print(f"Created {len(X_sequences)} sequences.")

# ==========================================================
# Pad
# ==========================================================

print("Padding sequences...")

X_padded = pad_sequences(
    X_sequences,
    padding="pre",
    dtype="float32"
)

y = np.array(y)

print("Sequence tensor:", X_padded.shape)
print("Labels:", y.shape)

# ==========================================================
# Save
# ==========================================================

np.save(
    OUTPUT / "X_lstm.npy",
    X_padded
)

np.save(
    OUTPUT / "y_lstm.npy",
    y
)

joblib.dump(
    MODEL_FEATURES,
    OUTPUT / "lstm_features.pkl"
)

print()

print("Saved:")
print("X_lstm.npy")
print("y_lstm.npy")
print("lstm_features.pkl")