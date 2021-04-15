import pytest
from random import randint
from model_bakery import baker


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('Student', _quantity=randint(1, 20), **kwargs)
    return factory


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('Course', **kwargs)
    return factory
