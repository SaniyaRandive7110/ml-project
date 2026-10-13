import os

import joblib
from flask import Flask, jsonify, request
from flask_cors import CORS

from train import MODEL_PATH, train

if not os.path.exists(MODEL_PATH):
    train()

model = joblib.load(MODEL_PATH)
app = Flask(__name__)
CORS(app)


def save_prediction(features, prediction):
    """Store the prediction in Postgres. Never breaks the API if the DB is down."""
    host = os.getenv("DB_HOST")
    if not host:
        return
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=host,
            dbname=os.getenv("DB_NAME", "predictions"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            connect_timeout=3,
        )
        with conn, conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS predictions ("
                "id SERIAL PRIMARY KEY, features TEXT, prediction INT, "
                "created_at TIMESTAMP DEFAULT NOW())"
            )
            cur.execute(
                "INSERT INTO predictions (features, prediction) VALUES (%s, %s)",
                (str(features), prediction),
            )
        conn.close()
    except Exception as e:
        print(f"DB save skipped: {e}")

@app.route("/")
def home():
    return jsonify(message="ML API is running", endpoints=["/health", "/predict"])


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    features = data.get("features")
    try:
        if not isinstance(features, list) or len(features) != 4:
            raise ValueError
        features = [float(x) for x in features]
    except (ValueError, TypeError):
        return jsonify(error='Send JSON like {"features": [5.1, 3.5, 1.4, 0.2]}'), 400

    pred = int(model.predict([features])[0])
    save_prediction(features, pred)
    return jsonify(prediction=pred)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)