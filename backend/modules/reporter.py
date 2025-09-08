import json
import csv
import os
from modules.utils import get_logger

logger = get_logger(__name__)

class ReportGenerator:
    def __init__(self, results):
        self.results = results

    def generate_json(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=4)
        logger.info(f"JSON report generated: {filepath}")

    def generate_csv(self, filepath):
        if not self.results:
            return
        keys = self.results[0].keys()
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.results)
        logger.info(f"CSV report generated: {filepath}")

    def generate_markdown(self, filepath):
        with open(filepath, 'w') as f:
            f.write("# FuzzGuard Scan Report\n\n")
            f.write("| Path | Status Code | Length | Technologies | Risk |\n")
            f.write("|------|-------------|--------|--------------|------|\n")
            for res in self.results:
                tech_str = ', '.join(res['technologies'])
                f.write(f"| {res['path']} | {res['status_code']} | {res['length']} | {tech_str} | {res['risk']} |\n")
        logger.info(f"Markdown report generated: {filepath}")