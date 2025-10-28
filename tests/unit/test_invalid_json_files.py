import json
import logging
import pytest
from server import load_json_data

"""Unit tests to check handling of invalid or missing JSON files for clubs and competitions
test1 : File not found -> warning logged, empty list returned
test2 : File found but invalid JSON structure -> warning logged, empty list returned
test3 : File found but key clubs is missing -> warning logged, empty list returned
test4 : Valid file with correct structure -> data returned correctly
"""

@pytest.fixture
def tmp_file(tmp_path):
    return tmp_path / "clubs.json"



def test_file_not_found(caplog):
    caplog.set_level(logging.WARNING)
    result = load_json_data("not_existing.json", "clubs")
    assert result == []
    assert "Unable to load not_existing.json" in caplog.text


def test_file_found_but_wrong_json_structure(tmp_file, caplog):
    caplog.set_level(logging.WARNING)
    tmp_file.write_text("{ clubs: }")
    result = load_json_data(tmp_file, "clubs")
    assert result == []
    assert f"Unable to load {tmp_file}" in caplog.text


def test_missing_clubs_key(tmp_file, caplog):
    caplog.set_level(logging.WARNING)
    tmp_file.write_text(json.dumps({"not_clubs": []}))
    result = load_json_data(tmp_file, "clubs")
    assert result == []
    assert f"Key 'clubs' not found in {tmp_file}" in caplog.text



def test_valid_file(tmp_file):
    clubs = [{"name": "Test Club", "email": "club@test.com", "points": 10}]
    tmp_file.write_text(json.dumps({"clubs": clubs}))
    result = load_json_data(tmp_file, "clubs")
    assert result == clubs
