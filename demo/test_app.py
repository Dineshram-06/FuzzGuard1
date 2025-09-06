from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Setup vulnerable directories/files
os.makedirs("admin", exist_ok=True)
with open("admin/index.html", "w") as f:
    f.write("<h1>Exposed Admin Panel</h1>")

os.makedirs("backup", exist_ok=True)
with open("backup/config.txt", "w") as f:
    f.write("DB_PASSWORD=secret123")

@app.route("/")
def index():
    return "Welcome to SIH1750 Test App"

@app.route("/admin/")
def admin():
    return send_from_directory("admin", "index.html")

@app.route("/backup/config.txt")
def config():
    return send_from_directory("backup", "config.txt")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)