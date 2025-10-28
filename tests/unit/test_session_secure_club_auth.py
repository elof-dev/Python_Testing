import server

"""
Unit test to chechk that the booking process uses the club from the session
and not the club sent in the form data (to prevent cheating)
Test1 : simulate club A logged in and trying to book places by sending club B in the form
result : booking should be made for club A and not club B
"""

def test_booking_uses_session_club(client):
    server.clubs = [{"name": "Club A", "points": "10"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "20"}]

    with client.session_transaction() as session:
        session['club_name'] = "Club A"

    response = client.post('/purchasePlaces', data={
        "competition": "Comp 1",
        "club": "Club B", 
        "places": "2"
    })

    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
    # Vérif que c'est bien le club A qui a perdu 2 points et pas le club B
    assert int(server.competitions[0]['numberOfPlaces']) == 18
    assert int(server.clubs[0]['points']) == 8




