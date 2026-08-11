def test_get_activities_returns_all(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert isinstance(activities["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"
    url = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    existing_email = "michael@mergington.edu"
    url = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(url, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_removes_participant(client):
    # Arrange
    email = "daniel@mergington.edu"
    url = "/activities/Chess%20Club/participants"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_missing_returns_404(client):
    # Arrange
    email = "unknown@mergington.edu"
    url = "/activities/Chess%20Club/participants"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_activity_not_found_returns_404(client):
    # Arrange
    email = "test@mergington.edu"
    signup_url = "/activities/Unknown%20Club/signup"
    unregister_url = "/activities/Unknown%20Club/participants"

    # Act
    signup_resp = client.post(signup_url, params={"email": email})
    unregister_resp = client.delete(unregister_url, params={"email": email})

    # Assert
    assert signup_resp.status_code == 404
    assert unregister_resp.status_code == 404
