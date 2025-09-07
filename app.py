from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Example data, you can modify or fetch from elsewhere
    total_scans = 128
    active_targets = 12
    high_risks = 5
    success_rate = 95
    
    return render_template('dashboard.html',
                           total_scans=total_scans,
                           active_targets=active_targets,
                           high_risks=high_risks,
                           success_rate=success_rate)

if __name__ == "__main__":
    app.run(debug=True)
