import os
import sys
import pytest


"""Pytest configuration file to set up the testing environment.
This file adds the project root directory to sys.path to ensure that
"""

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from server import app

@pytest.fixture
def client():
    """Flask test client fixture.
    Provides a test client for the Flask application defined in server.py.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client