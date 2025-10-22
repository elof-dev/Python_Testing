import server

"""
Unit test file to verify that club points are correctly updated after booking.

Test 1: Club has 10 points, books 3 places, points should decrease by 3.
    - status code 200
    - success message "Great - booking complete!"
    - club points decrease by 3

"""


def test_club_points_decrease_after_booking(client):
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

