import os
import tempfile
import pytest
from app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

def test_upload_files(client):
    data = {
        'videos': [
            (open('tests/video1.mp4', 'rb'), 'video1.mp4'),
            (open('tests/video2.mp4', 'rb'), 'video2.mp4'),
            (open('tests/video3.mp4', 'rb'), 'video3.mp4'),
            (open('tests/video4.mp4', 'rb'), 'video4.mp4')
        ]
    }
    rv = client.post('/upload', data=data, content_type='multipart/form-data')
    assert rv.status_code == 200
    assert b'north' in rv.data
    assert b'south' in rv.data
    assert b'west' in rv.data
    assert b'east' in rv.data