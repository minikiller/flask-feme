from abc import ABC
from operator import add

from .base import Example


class Datastore(ABC):

    def __init__(self, _db=None):
        self.session = None
        if _db:
            self.session = _db.session

    def add(self, resource):
        self.session.add(resource)
        return self.session.commit()

    def update(self):
        return self.session.commit()

    def delete(self, resource):
        self.session.delete(resource)
        return self.session.commit()


class ExampleDatastore(Datastore):

    def __init__(self, _db):
        super().__init__(_db)

    def create_example(self, name):
        ex = Example(name=name,sex="female")
        super().add(ex)
