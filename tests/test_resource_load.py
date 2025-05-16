import pytest
from .load_resource import test_stations, test_earthquakes

def test_load_test_items(test_stations, test_earthquakes):
    assert len(test_stations) >0
    assert len(test_earthquakes) >0
