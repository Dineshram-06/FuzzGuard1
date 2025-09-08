from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the vulnerable test app!"

@app.route('/admin')
def admin():
    return "Admin panel - secret content!"

@app.route('/backup.txt')
def backup():
    return "Backup data: sensitive info here."

@app.route('/config.json')
def config():
    return '{"db": "mysql", "password": "1234"}'

if __name__ == '__main__':
    app.run(debug=True, port=5001)