from pathlib import Path

from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)

def test_frontend_requests_fresh_activity_data_after_signup():
    app_js = Path("src/static/app.js").read_text(encoding="utf-8")

    assert 'fetch("/activities", { cache: "no-store" })' in app_js


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert unregister_response.status_code == 200

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]
