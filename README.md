# DevOps Mid Assignment - Submission Portal

A Flask assignment submission portal with automated tests and GitHub Actions CI.

## Features
- Submit student name, registration number, assignment title, and URL.
- Validate required fields and submission URLs.
- Display saved submissions.
- Run automated tests on every push.
- Generate JSON reports for passing and failing test runs.
- Send reports to a local receiver through Cloudflare Tunnel.

## Setup
Activate the virtual environment and install dependencies:

    source .venv/bin/activate
    pip install -r requirements.txt

## Run the Portal

    python app.py

Open http://127.0.0.1:5000 in your browser.

## Run Tests

    python -m pytest -v

Generate the JSON report:

    python run_tests.py

## Start the Local Report Receiver

Set the report token and start the receiver:

    export REPORT_TOKEN="your-secret-token"
    python receiver.py

The receiver listens on port 5001 and saves reports to testreport.json.

## Send Reports from GitHub Actions

Start Cloudflare Tunnel in another terminal:

    cloudflared tunnel --url http://127.0.0.1:5001

Configure these repository secrets in GitHub Settings > Secrets and variables > Actions:

- REPORT_RECEIVER_URL: your Cloudflare HTTPS URL
- REPORT_TOKEN: the same token used by the receiver

Keep the receiver and tunnel running during the demonstration.

## Continuous Integration

GitHub Actions runs tests on every push. It generates a JSON report for both passing and failing test runs and attempts to send the report to the local receiver.

The report includes repository name, branch, commit SHA, pipeline run ID, timestamp, individual test results, test counts, and overall status.
