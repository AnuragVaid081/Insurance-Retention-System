from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "Synthetic Generator" / "data"

dataset = pd.read_csv(
    DATA_DIR / "model_dataset.csv"
)

print(dataset.info())


print(dataset.isnull().sum())


print(dataset["Renewed"].value_counts())

print(
    dataset["Renewed"].value_counts(normalize=True)
)


print(dataset.describe())



numeric = dataset.select_dtypes(include="number")

print(
    numeric.corr()["Renewed"]
    .sort_values(ascending=False)
)