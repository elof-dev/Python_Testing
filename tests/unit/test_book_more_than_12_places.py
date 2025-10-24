import server

"""
Unit test file to check that clubs cannot book more than 12 places in total.

Test 1: Club A books exactly 12 places -> success
Test 2: Club A tries to book 13 places -> rejected
Test 3: Club A has already booked 6 places, tries to book 7 more -> rejected (cumulative > 12)
Test 4: Club A has already booked 6 places, tries to book 5 more -> accepted (cumulative = 11)
"""


def test_book_12_places_allowed(client):
    server.clubs = [{"name": "Club A", "points": "13"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "25"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '12'
    })

    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 13


def test_cannot_book_more_than_12_places(client):
    server.clubs = [{"name": "Club A", "points": "13"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "25"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '13'
    })

    assert response.status_code == 200
    assert b"Cannot book more than" in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 25


def test_cannot_exceed_12_places_cumulatively(client):
    server.clubs = [{"name": "Club A", "points": "13"}]
    server.competitions = [{
        "name": "Comp 1",
        "numberOfPlaces": "25",
        "booked_by": {"Club A": 6}
    }]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '7'
    })

    assert response.status_code == 200
    assert b"Cannot book more than" in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 25
    assert int(server.clubs[0]['points']) == 13


def test_booking_allowed_when_cumulative_under_limit(client):
    server.clubs = [{"name": "Club A", "points": "13"}]
    server.competitions = [{
        "name": "Comp 1",
        "numberOfPlaces": "25",
        "booked_by": {"Club A": 6}
    }]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '5'
    })

    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 20
    assert int(server.clubs[0]['points']) == 8
    assert server.competitions[0]['booked_by']['Club A'] == 11
