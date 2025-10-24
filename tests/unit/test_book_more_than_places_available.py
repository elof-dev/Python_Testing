import server

"""
Unit test to verify that users cannot book more places than available.
"""

def test_booking_more_places_than_available(client):
    server.clubs = [{"name": "Club A", "points": "20"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "5"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '10'
    })

    assert response.status_code == 200
    assert b"Cannot book more places than available." in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 5
    assert int(server.clubs[0]['points']) == 20
