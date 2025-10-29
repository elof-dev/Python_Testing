
"""Unit tests for the logout functionality
test1: Logout gives a redirect response
test2: logout redirects to index
test3: logout clears session data
"""



def test_logout_redirects(client):
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302

def test_logout_redirects_to_index(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

def test_logout_clears_session(client):
    with client.session_transaction() as session:
        session['club_name'] = 'Club A'

    client.get('/logout')
    with client.session_transaction() as session:
        assert session.get('club_name') is None


