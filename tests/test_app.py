import app as app_module


def setup_function():
    app_module.submissions.clear()


def test_valid_submission_is_saved_and_displayed():
    client = app_module.app.test_client()

    response = client.post("/", data={
        "name": "Saad Shah",
        "registration_number": "sp23-bcs-012",
        "assignment_title": "DevOps Mid",
        "submission_url": "https://github.com/"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Saad Shah" in response.data
    assert b"sp23-bcs-012" in response.data
    assert b"DevOps Mid" in response.data
    assert b"https://github.com/" in response.data
    assert len(app_module.submissions) == 2



def test_missing_registration_number_is_rejected():
    client = app_module.app.test_client()

    response = client.post("/", data={
        "name": "Saad Shah",
        "registration_number": "",
        "assignment_title": "DevOps Mid",
        "submission_url": "https://github.com/"
    })

    assert response.status_code == 200
    assert b"All fields are required." in response.data
    assert len(app_module.submissions) == 0


def test_invalid_submission_url_is_rejected():
    client = app_module.app.test_client()

    response = client.post("/", data={
        "name": "Saad Shah",
        "registration_number": "sp23-bcs-012",
        "assignment_title": "DevOps Mid",
        "submission_url": "not-a-url"
    })

    assert response.status_code == 200
    assert b"Please enter a valid HTTP or HTTPS URL." in response.data
    assert len(app_module.submissions) == 0
