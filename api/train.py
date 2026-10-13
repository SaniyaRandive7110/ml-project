import os
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")


def train():
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"Model accuracy: {acc:.2f}")
    joblib.dump(model, MODEL_PATH)
    print(f"Saved {MODEL_PATH}")


if __name__ == "__main__":
    train()