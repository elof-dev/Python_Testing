import server

"""
Unit test file to check if the index page displays the clubs and their points correctly
Test 1: The page loads successfully (status code 200)
Test 2: Each club name and its points appear in the HTML
"""

def test_index_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Clubs Points Summary" in response.data


def test_index_page_displays_clubs_points(client):
    response = client.get('/')
    data = response.data.decode()

    for club in server.clubs:
        assert club["name"] in data
        assert club["points"] in data
