from flask import Flask, render_template, request, redirect, url_for
from urllib.parse import urlparse

app = Flask(__name__)

# In-memory storage for submissions
submissions = []


def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc) and "." in parsed.netloc
    except ValueError:
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        registration_number = request.form.get("registration_number", "").strip()
        assignment_title = request.form.get("assignment_title", "").strip()
        submission_url = request.form.get("submission_url", "").strip()

        if not all([name, registration_number, assignment_title, submission_url]):
            error = "All fields are required."
        elif not is_valid_url(submission_url):
            error = "Please enter a valid HTTP or HTTPS URL."
        else:
            submissions.append({
                "name": name,
                "registration_number": registration_number,
                "assignment_title": assignment_title,
                "submission_url": submission_url,
            })
            return redirect(url_for("index"))

    return render_template("index.html", submissions=submissions, error=error)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
