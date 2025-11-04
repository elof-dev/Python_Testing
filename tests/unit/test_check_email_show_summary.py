"""Unit tests for the /showSummary route in server.py.
test1 : Valid email should return 200 and welcome message
test2 : Unknown email should return 200 and error message
test3 : Invalid email (empty or whitespace) should return 200 and error message

"""
import server


def test_show_summary_with_valid_email(client):
    server.clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co"}
    ]
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome, john@simplylift.co' in response.data


def test_show_summary_with_unknown_email(client):
    server.clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co"}
    ]
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    assert response.status_code == 200
    assert b"Sorry, that email was not found" in response.data


def test_show_summary_with_invalid_email(client):
    server.clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co"}
    ]
    response = client.post('/showSummary', data={'email': '   '})
    assert response.status_code == 200
    assert b"Sorry, that email was not found" in response.data