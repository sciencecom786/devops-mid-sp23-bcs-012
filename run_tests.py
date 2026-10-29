import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET


REPORT_FILE = Path("testreport.json")
XML_FILE = Path("test-results.xml")


def main():
    start_time = datetime.now(timezone.utc).isoformat()

    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "-v", "--junitxml", str(XML_FILE)
    ])

    tests = []

    if XML_FILE.exists():
        root = ET.parse(XML_FILE).getroot()

        for case in root.iter("testcase"):
            failure = case.find("failure")
            error = case.find("error")
            problem = failure if failure is not None else error

            if problem is not None:
                status = "failed"
                message = problem.get("message", "") or (problem.text or "").strip()
            elif case.find("skipped") is not None:
                status = "skipped"
                message = case.find("skipped").get("message", "")
            else:
                status = "passed"
                message = ""

            tests.append({
                "name": f"{case.get('classname', '')}::{case.get('name', '')}",
                "result": status,
                "failure_message": message
            })

    passed = sum(t["result"] == "passed" for t in tests)
    failed = sum(t["result"] == "failed" for t in tests)
    skipped = sum(t["result"] == "skipped" for t in tests)

    report = {
        "repository_name": os.getenv("GITHUB_REPOSITORY", "DevOpsMid"),
        "branch": os.getenv("GITHUB_REF_NAME", "local"),
        "commit_sha": os.getenv("GITHUB_SHA", "local"),
        "pipeline_run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "timestamp": start_time,
        "tests": tests,
        "total_tests": len(tests),
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "overall_status": "passed" if result.returncode == 0 else "failed"
    }

    REPORT_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nTest report saved to: {REPORT_FILE.resolve()}")
    print(json.dumps(report, indent=2))

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
