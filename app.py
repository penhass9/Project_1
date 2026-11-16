from flask import Flask
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "visitsdb")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

POD_NAME = os.getenv("HOSTNAME", "unknown")


def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():
    conn = get_db_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO visits (visit_time) VALUES (NOW())"
        )

        cur.execute("SELECT COUNT(*) FROM visits")

        total_visits = cur.fetchone()[0]

        conn.commit()
        cur.close()

        return f"""
        <h1>Flask + PostgreSQL Application</h1>
        <h2>Total Visits: {total_visits}</h2>
        <h3>Served by Pod: {POD_NAME}</h3>
        """

    finally:
        conn.close()


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
