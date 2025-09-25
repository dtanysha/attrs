import pytest
import attr

def non_negative(_instance, _attribute, value):
    if value < 0:
        raise ValueError("age must be non-negative")

@attr.define
class Person:
    name: str = attr.field(converter=str)
    age: int = attr.field(converter=int, validator=non_negative)
    tags: list[str] = attr.field(factory=list)

def test_validation_and_conversion_ok():
    p = Person(name=123, age="5")
    assert p.name == "123"
    assert p.age == 5

def test_validation_error_on_negative_age():
    with pytest.raises(ValueError):
        Person("Ann", -1)

def test_factory_independent_lists():
    p1 = Person("A", 1)
    p2 = Person("B", 2)
    p1.tags.append("x")
    assert p1.tags == ["x"]
    assert p2.tags == []

@attr.define(frozen=True)
class Point:
    x: int
    y: int

def test_frozen_prevents_assignment():
    pt = Point(1, 2)
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        pt.x = 3

@attr.define(slots=True, order=True, frozen=True)
class Item:
    price: int
    title: str

def test_slots_and_ordering_and_hash_set():
    a = Item(10, "a")
    b = Item(5, "b")
    c = Item(10, "a")
    assert sorted([a, b]) == [b, a]
    assert a == c
    assert len({a, c}) == 1

def forbid_empty_name(instance, attribute, value):
    if attribute.name == "name" and value == "":
        raise ValueError("empty name")

@attr.define(on_setattr=[forbid_empty_name])
class User:
    name: str
    age: int = 0

def test_on_setattr_business_rule():
    u = User("Bob")
    with pytest.raises(ValueError):
        u.name = ""
