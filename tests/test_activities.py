def test_get_activities_returns_all(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    email = "newstudent@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400(client):
    existing_email = "michael@mergington.edu"
    response = client.post("/activities/Chess%20Club/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_participant(client):
    email = "daniel@mergington.edu"
    response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_returns_404(client):
    email = "unknown@mergington.edu"
    response = client.delete("/activities/Chess%20Club/participants", params={"email": email})

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_activity_not_found_returns_404(client):
    signup_resp = client.post("/activities/Unknown%20Club/signup", params={"email": "test@mergington.edu"})
    unregister_resp = client.delete("/activities/Unknown%20Club/participants", params={"email": "test@mergington.edu"})

    assert signup_resp.status_code == 404
    assert unregister_resp.status_code == 404
