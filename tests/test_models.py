from app.models import Example
from app.models.datastore import ExampleDatastore
from app.models.trade import Trade


# def test_create_example(db):
#     datastore = ExampleDatastore(db)
#     datastore.create_example('test')
#
#     ex = db.session.query(Example).filter_by(name='test').first()
#     assert ex


def test_add_trade(db):
    trade = Trade(name="hello", symbol="symbol")
    trade.add(trade)

    query = Trade.query.get(trade.id)
    assert query


def test_delete_trade(db):
    trade = Trade(name="hello1", symbol="symbol1")
    trade.add(trade)

    query = Trade.query.get(trade.id)
    assert query

    trade.delete(trade)
    query = Trade.query.get(trade.id)
    # assert query
    assert query == None
