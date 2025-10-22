import server

"""
Unit test file to check that clubs cannot book more than 12 places.

Test 1: Club A has 13 points and competition 1 has 25 places.
    - Book 12 places
    - status code 200
    - message: "Great - booking complete!"
    - competition places decreased

Test 2: Club A has 13 points and competition 1 has 25 places.
    - Book 13 places
    - status code 200
    - message contains "Cannot book more than"
    - competition places unchanged
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