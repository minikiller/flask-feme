from flask.testing import FlaskClient


def test_example_page(client: FlaskClient):
    res = client.get('/api/v1/trades')
    assert res.ok
    # assert res.json == {'message': 'Success'}
