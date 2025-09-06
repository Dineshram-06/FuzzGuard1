import json
import csv
from datetime import datetime
from typing import List, Dict

class ReportEngine:
    def __init__(self, findings: List[Dict], target_url: str, tech_stack: List[str], elapsed: float):
        self.findings = findings
        self.target_url = target_url
        self.tech_stack = tech_stack
        self.elapsed = elapsed
        self.timestamp = datetime.now().isoformat()

    def save_json(self, filename: str):
        report = {
            "metadata": {
                "target": self.target_url,
                "technologies": self.tech_stack,
                "timestamp": self.timestamp,
                "duration_seconds": self.elapsed
            },
            "findings": self.findings
        }
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)

    def save_markdown(self, filename: str):
        with open(filename, "w") as f:
            f.write("# SIH1750 Web Fuzzer Report\n\n")
            f.write(f"**Target:** {self.target_url}\n")
            f.write(f"**Technologies:** {', '.join(self.tech_stack or ['None'])}\n")
            f.write(f"**Scan Duration:** {self.elapsed:.1f} seconds\n")
            f.write(f"**Timestamp:** {self.timestamp}\n\n")
            f.write("## Executive Summary\n")
            high_risk = sum(1 for f in self.findings if f.get("risk") == "High")
            f.write(f"Discovered {len(self.findings)} findings, including {high_risk} high-risk items. Immediate action recommended for high-risk findings.\n\n")
            f.write("## Detailed Findings\n")
            for finding in self.findings:
                f.write(f"- **{finding['url']}** (Status: {finding['status']}, Type: {finding['type']}, Risk: {finding.get('risk', 'Low')})\n")

    def save_csv(self, filename: str):
        with open(filename, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["url", "status", "type", "risk", "length"])
            writer.writeheader()
            for finding in self.findings:
                writer.writerow({
                    "url": finding["url"],
                    "status": finding["status"],
                    "type": finding["type"],
                    "risk": finding.get("risk", "Low"),
                    "length": finding["length"]
                })