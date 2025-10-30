import server
from datetime import datetime, timedelta

"""
Unit test file to check that booking is not allowed for past competitions

Test 1: A competition in the future -> user can access booking page
    - status code 200
    - page contains "How many places?"
Test 2: A competition in the past -> booking is refused.
    - status code 200
    - message contains "This competition has already taken place"
"""

def test_can_book_future_competition(client):
    future_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    server.competitions = [{"name": "Future Comp", "date": future_date, "numberOfPlaces": "10"}]
    server.clubs = [{"name": "Club A", "email": "a@a.com", "points": "10"}]

    response = client.get('/book/Future Comp')

    assert response.status_code == 200
    assert b"How many places?" in response.data


def test_cannot_book_past_competition(client):
    past_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")
    server.competitions = [{"name": "Old Comp", "date": past_date, "numberOfPlaces": "10"}]
    server.clubs = [{"name": "Club A", "email": "a@a.com", "points": "10"}]

    response = client.get('/book/Old Comp')

    assert response.status_code == 200
    assert b"This competition has already taken place" in response.data
