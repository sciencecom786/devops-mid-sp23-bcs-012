import hmac
import json
import os
from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)
REPORT_FILE = Path(__file__).resolve().parent / "testreport.json"
REPORT_TOKEN = os.environ.get("REPORT_TOKEN", "")


@app.route("/report", methods=["POST"])
def receive_report():
    if not REPORT_TOKEN:
        return jsonify({"error": "Receiver token is not configured"}), 500

    supplied_token = request.headers.get("X-Report-Token", "")

    if not hmac.compare_digest(supplied_token, REPORT_TOKEN):
        return jsonify({"error": "Unauthorized"}), 401

    report = request.get_json(silent=True)

    if not isinstance(report, dict):
        return jsonify({"error": "Invalid JSON report"}), 400

    required_fields = [
        "repository_name",
        "branch",
        "commit_sha",
        "pipeline_run_id",
        "timestamp",
        "tests",
        "total_tests",
        "passed",
        "failed",
        "overall_status",
    ]

    if not all(field in report for field in required_fields):
        return jsonify({"error": "Report is missing required fields"}), 400

    REPORT_FILE.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"Received report: {REPORT_FILE}")
    return jsonify({
        "message": "Report received and saved",
        "file": str(REPORT_FILE),
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
