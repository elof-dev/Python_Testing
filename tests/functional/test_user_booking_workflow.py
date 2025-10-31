import server

"""
Functional test to check the user workflow from login to logout

    1. User logs in
    2. User accesses booking page
    3. User books places
    4. User verifies their points decreased and competition places decreased
    5. User logs out
"""


def test_full_booking_workflow(client):
    server.clubs = [{"name": "Simply Lift", "email": "john@simplylift.co", "points": "20"}]
    server.competitions = [{"name": "Fall Classic", "date": "2026-10-22 13:30:00", "numberOfPlaces": "10"}]
    
    # Step 1: User logs in
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b"Welcome" in response.data
    
    with client.session_transaction() as session:
        assert session['club_name'] == "Simply Lift"
    
    # Step 2: User accesses booking page
    response = client.get('/book/Fall Classic')
    assert response.status_code == 200
    assert b"How many places?" in response.data
    assert b"Fall Classic" in response.data
    
    # Step 3: User books places
    response = client.post('/purchasePlaces', data={
        'competition': 'Fall Classic',
        'places': '5'
    })
    assert response.status_code == 200
    assert b"Great - booking complete!" in response.data
    
    # Step 4: Verify data was updated : user's points should decrease from 20 to 15
    # Competition places should decrease from 10 to 5
    # Booking tracking should be recorded
    assert int(server.clubs[0]['points']) == 15
    assert int(server.competitions[0]['numberOfPlaces']) == 5
    assert server.competitions[0]['booked_by']['Simply Lift'] == 5
    
    # Step 5: User logs out
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    
    with client.session_transaction() as session:
        assert session.get('club_name') is None

