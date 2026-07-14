from pathlib import Path

import joblib
import pandas as pd

from training_features import MODEL_FEATURES

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import(
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
from sklearn.tree import DecisionTreeClassifier

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "Synthetic Generator" / "data"

MODEL_DIR = PROJECT_ROOT / "models" / "saved_models"

MODEL_DIR.mkdir(exist_ok= True)

INPUT_PATH = DATA_DIR / "model_dataset.csv"

def train_model():
    dataset = pd.read_csv(INPUT_PATH)

    dataset = dataset.drop(
        columns= [
            "Policy_Number",
            "RID",
            "RED",
            "Vehicle_First_Registration_Date",
            "Portfolio_Size"    
        ],
        errors= "ignore"
    )

    X = dataset[MODEL_FEATURES]

    y = dataset["Renewed"]

    categorical_columns = X.select_dtypes(
        include= ["object","string"]
    ).columns.to_list()

    print(categorical_columns)


    preprocessor =  ColumnTransformer(
        transformers=[
            (
                "categorical",
                OrdinalEncoder(
                    handle_unknown="use_encoded_value",
                    unknown_value= -1
                ),

                categorical_columns
            )

        ],
        remainder="passthrough"
    )

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size= 0.20, random_state= 42, stratify= y)

    models = {
        #"Logistic Regression": LogisticRegression(max_iter= 1000),
        #"Decision Tree": DecisionTreeClassifier(random_state = 42),
        "Random Forest": RandomForestClassifier(
            n_estimators = 200,
            random_state = 42
           
        )
    }

    for name, model in models.items():
        pipeline = Pipeline(
           steps = [
               ("preprocessor", preprocessor),
               ("model", model)
           ]
       )
       
        pipeline.fit(X_train,y_train)

        X_processed = pipeline.named_steps["preprocessor"].transform(X_train)

        predictions = pipeline.predict(X_test)

        feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

        print(feature_names)

        filename = (
            name.lower()
            .replace(" ", "_")
            + ".pkl"
    )

        joblib.dump(
            pipeline,
            MODEL_DIR / filename
    )
        
        joblib.dump(
            X_processed,
            MODEL_DIR / "background_processed.pkl"
)
        joblib.dump(
            pipeline.named_steps["preprocessor"],
            MODEL_DIR / "preprocessor.pkl"
        )

        joblib.dump(
            pipeline.named_steps["model"],
            MODEL_DIR / "random_forest_model.pkl"
        )
                
        feature_names = (
            pipeline.named_steps["preprocessor"]
            .get_feature_names_out()
        )

        importances = (
            pipeline.named_steps["model"]
            .feature_importances_
        )

        importance_df = (
            pd.DataFrame({
                "Feature": feature_names,
                "Importance": importances
            })
            .sort_values("Importance", ascending=False)
        )

        print(importance_df.head(20))

        print("\nAccuracy")

        print(
            accuracy_score(
                y_test,
                predictions
            )
        )

        print("\nPrecision")

        print(
            precision_score(
                y_test,
                predictions
            )
        )

        print("\nRecall")

        print(
            recall_score(
                y_test,
                predictions
            )
        )

        print("\nF1 Score")

        print(
            f1_score(
                y_test,
                predictions
            )
        )

        print("\nConfusion Matrix")

        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        print("\nClassification Report")

        print(
            classification_report(
                y_test,
                predictions
            )
        )

        

        print(f"{name} saved successfully.")

        print("\nModel saved succesfully")

        
if __name__ == "__main__":

    train_model()