import server

"""
Unit test file for the place booking feature.
The purpose is to verify that booking places is only possible with sufficient points.

Test 1: the club has 4 points and wants to book 4 places — booking accepted :
    - status code 200
    - confirmation message
    - remaining places updated correctly.
Test 2: the club has 4 points and wants to book 5 places — booking refused :
    - status code 200
    - error message
    - remaining places unchanged
"""


def test_book_places_with_enough_points(client):
    server.clubs = [{"name": "Club A", "points": "4"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "5"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '4'
    })

    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 1

def test_book_places_without_enough_points(client):
    server.clubs = [{"name": "Club B", "points": "4"}]
    server.competitions = [{"name": "Comp 2", "numberOfPlaces": "5"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 2',
        'club': 'Club B',
        'places': '5'
    })

    assert response.status_code == 200
    assert b"Cannot book more places than club points." in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 5