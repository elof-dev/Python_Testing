import server

"""
Unit test file to verify that the booking system correctly handles invalid number of places inputs

Test 1: booking with valid number of places -> success, points and places updated
Test 2 :booking with 0 places -> error message, number of places and points unchanged
Test 3: booking with negative places -> error message, number of places and points unchanged
Test 4: booking without providing number of places -> error message, number of places and points unchanged
Test 5: booking with non-numeric input -> error message, number of places and points unchanged
"""

def test_booking_valid_number_of_places(client):
    server.clubs = [{"name": "Club A", "points": "10"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "20"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '3'
    })

    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
    assert int(server.clubs[0]['points']) == 7
    assert int(server.competitions[0]['numberOfPlaces']) == 17


def test_booking_zero_places(client):
    server.clubs = [{"name": "Club A", "points": "10"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "20"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '0'
    })

    assert response.status_code == 200
    assert b"Invalid number of places." in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 20
    assert int(server.clubs[0]['points']) == 10


def test_booking_negative_places(client):
    server.clubs = [{"name": "Club A", "points": "10"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "20"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '-5'
    })

    assert response.status_code == 200
    assert b"Invalid number of places." in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 20
    assert int(server.clubs[0]['points']) == 10


def test_booking_without_places_value(client):
    server.clubs = [{"name": "Club A", "points": "10"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "20"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': ''
    })

    assert response.status_code == 200
    assert b"Please enter a number of places." in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 20
    assert int(server.clubs[0]['points']) == 10


def test_booking_with_non_numeric_input(client):
    server.clubs = [{"name": "Club A", "points": "10"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "20"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': 'abc'
    })

    assert response.status_code == 200
    assert b"Invalid number of places." in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 20
    assert int(server.clubs[0]['points']) == 10
