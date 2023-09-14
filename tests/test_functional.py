from fastapi.testclient import TestClient
from main import app


client = TestClient(app)

def test_health_check():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}

def test_graphql_hello():
    response = client.post(
        '/graphql', 
        json={'query': '{hello}'},
    )
    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'hello': 'Hello World!'
        }
    }

def test_graphql_hello_name():
    response = client.post(
        '/graphql', 
        json={'query': '{hello (name: "User")}'},
    )
    assert response.status_code == 200
    assert response.json() == {
        'data': {
            'hello': 'Hello User!'
        }
    }