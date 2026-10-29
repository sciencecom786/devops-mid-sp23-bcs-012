import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def main():
    receiver_url = os.environ.get("REPORT_RECEIVER_URL", "").rstrip("/")
    token = os.environ.get("REPORT_TOKEN", "")
    report_path = Path("testreport.json")

    if not receiver_url or not token:
        print("REPORT_RECEIVER_URL and REPORT_TOKEN must be configured.")
        return 1

    if not report_path.exists():
        print("testreport.json was not found.")
        return 1

    request = urllib.request.Request(
        f"{receiver_url}/report",
        data=report_path.read_bytes(),
        headers={
            "Content-Type": "application/json",
            "X-Report-Token": token,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            print(response.read().decode("utf-8"))
            return 0
    except (urllib.error.URLError, TimeoutError) as error:
        print(f"Failed to send report: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
