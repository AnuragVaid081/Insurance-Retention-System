from pathlib import Path

import pandas as pd
import joblib
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    average_precision_score,
    roc_curve,
    precision_recall_curve
)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Masking,
    LSTM,
    Dense,
    Dropout,
)
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
)

# ==========================================================
# Paths
# ==========================================================

ROOT = Path(__file__).resolve().parent.parent

MODEL_DIR = ROOT / "saved_models"

X = np.load(MODEL_DIR / "X_lstm.npy")
y = np.load(MODEL_DIR / "y_lstm.npy")

print("Dataset Loaded")
print(X.shape)
print(y.shape)

# ==========================================================
# Train Test Split
# ==========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# ==========================================================
# Model
# ==========================================================

model = Sequential([

    Masking(mask_value=0.0),

    LSTM(
        64,
        return_sequences=False,
    ),

    Dropout(0.40),

    Dense(
        32,
        activation="relu",
    ),

    Dropout(0.30),

    Dense(
        16,
        activation="relu",
    ),

    Dense(
        1,
        activation="sigmoid",
    ),
])

# ==========================================================
# Compile
# ==========================================================

model.compile(

    optimizer="adam",

    loss="binary_crossentropy",

    metrics=[

        "accuracy",

        tf.keras.metrics.Precision(),

        tf.keras.metrics.Recall()

    ]
)

model.summary()

# ==========================================================
# Callbacks
# ==========================================================

callbacks = [

    EarlyStopping(

        monitor="val_loss",

        patience=10,

        restore_best_weights=True

    ),

    ModelCheckpoint(

        MODEL_DIR / "lstm_model.keras",

        monitor="val_loss",

        save_best_only=True

    )

]

# ==========================================================
# Train
# ==========================================================

history = model.fit(

    X_train,

    y_train,

    validation_split=0.20,

    epochs=35,

    batch_size=32,

    callbacks=callbacks,

    verbose=1

)

history_df = pd.DataFrame(history.history)

history_df.to_csv(
    MODEL_DIR / "lstm_training_history.csv",
    index=False
)
# ==========================================================
# Evaluation
# ==========================================================

probabilities = model.predict(X_test).flatten()

predictions = (probabilities >= 0.5).astype(int)

print()

print("Accuracy")
print(
    accuracy_score(
        y_test,
        predictions
    )
)

print()

print("Precision")
print(
    precision_score(
        y_test,
        predictions
    )
)

print()

print("Recall")
print(
    recall_score(
        y_test,
        predictions
    )
)

print()

print("F1 Score")
print(
    f1_score(
        y_test,
        predictions
    )
)

print()

roc_auc = roc_auc_score(
    y_test,
    probabilities
)

print()

print("ROC-AUC")

print(roc_auc)

pr_auc = average_precision_score(
    y_test,
    probabilities
)

print()

print("PR-AUC")

print(pr_auc)

print()



print("Confusion Matrix")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print()

print(
    classification_report(
        y_test,
        predictions
    )
)

print()

fpr, tpr, _ = roc_curve(
    y_test,
    probabilities
)

plt.figure(figsize=(8,6))

plt.plot(
    fpr,
    tpr,
    label=f"AUC = {roc_auc:.3f}"
)

plt.plot(
    [0,1],
    [0,1],
    "--"
)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title("ROC Curve")

plt.legend()

plt.show()

print()

precision, recall, _ = precision_recall_curve(
    y_test,
    probabilities
)

plt.figure(figsize=(8,6))

plt.plot(
    recall,
    precision
)

plt.xlabel("Recall")

plt.ylabel("Precision")

plt.title("Precision Recall Curve")

plt.show()

print()

plt.figure(figsize=(8,6))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.title("Training vs Validation Loss")

plt.legend()

plt.show()

print()

plt.figure(figsize=(8,6))

plt.plot(
    history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epoch")

plt.ylabel("Accuracy")

plt.title("Training vs Validation Accuracy")

plt.legend()

plt.show()

print("LSTM Model Saved Successfully")