from flask import Flask, request, jsonify, send_from_directory
import threading
import time
import os
from modules.scanner import WebApplicationFuzzer
from modules.detector import TechnologyDetector
from modules.reporter import ReportGenerator
from modules.utils import get_logger, load_wordlist

app = Flask(__name__)
logger = get_logger(__name__)

# Global state for scan
scan_status = {
    "state": "idle",
    "progress": 0,
    "results": [],
    "error": None,
    "report_files": {}
}

reports_dir = os.path.join(os.path.dirname(__file__), 'reports')
os.makedirs(reports_dir, exist_ok=True)

def run_scan(url, threads, rate):
    global scan_status
    scan_status["state"] = "running"
    scan_status["progress"] = 0
    scan_status["results"] = []
    scan_status["error"] = None
    scan_status["report_files"] = {}

    try:
        wordlist = load_wordlist()
        total_paths = len(wordlist)
        fuzzer = WebApplicationFuzzer(url, threads, rate)
        detector = TechnologyDetector()

        def callback(path, response):
            if response:
                tech = detector.detect(response)
                result = {
                    "path": path,
                    "status_code": response.status_code,
                    "length": len(response.content),
                    "technologies": tech,
                    "risk": assess_risk(path, response.status_code)
                }
                scan_status["results"].append(result)
            scan_status["progress"] = (len(scan_status["results"]) / total_paths) * 100

        fuzzer.fuzz(wordlist, callback)

        # Generate reports
        reporter = ReportGenerator(scan_status["results"])
        timestamp = int(time.time())
        json_file = f"report_{timestamp}.json"
        csv_file = f"report_{timestamp}.csv"
        md_file = f"report_{timestamp}.md"

        reporter.generate_json(os.path.join(reports_dir, json_file))
        reporter.generate_csv(os.path.join(reports_dir, csv_file))
        reporter.generate_markdown(os.path.join(reports_dir, md_file))

        scan_status["report_files"] = {
            "json": json_file,
            "csv": csv_file,
            "md": md_file
        }

        scan_status["state"] = "completed"
    except Exception as e:
        scan_status["state"] = "error"
        scan_status["error"] = str(e)
        logger.error(f"Scan error: {e}")

def assess_risk(path, status_code):
    sensitive_paths = ['/admin', '/backup', '/config', '/db']
    if any(p in path for p in sensitive_paths) and status_code == 200:
        return "high"
    elif status_code in [200, 301]:
        return "medium"
    else:
        return "low"

@app.route('/api/start', methods=['POST'])
def start_scan():
    if scan_status["state"] == "running":
        return jsonify({"error": "Scan already running"}), 400

    data = request.json
    url = data.get('url')
    threads = data.get('threads', 5)
    rate = data.get('rate', 10)  # requests per second

    if not url:
        return jsonify({"error": "URL required"}), 400

    threading.Thread(target=run_scan, args=(url, threads, rate)).start()
    return jsonify({"message": "Scan started"})

@app.route('/api/status', methods=['GET'])
def get_status():
    return jsonify(scan_status)

@app.route('/api/report/<filename>', methods=['GET'])
def get_report(filename):
    return send_from_directory(reports_dir, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)