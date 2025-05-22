import tests.resources
from importlib.resources import files
import pytest
import heatmap

@pytest.fixture(scope="module")
def test_stations():
    sta_file = files(tests.resources).joinpath("test_stations.txt")
    return heatmap.read_stations_adept(sta_file)

@pytest.fixture(scope="module")
def test_stations_lat():
    sta_file = files(tests.resources).joinpath("test_stations_lat.txt")
    return heatmap.read_stations_adept(sta_file)



@pytest.fixture(scope="module")
def test_earthquakes():
    eq_file = files(tests.resources).joinpath("test_earthquakes.txt")
    return heatmap.read_earthquakes_adept(eq_file)
