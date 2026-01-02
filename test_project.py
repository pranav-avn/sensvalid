from project import raw_to_voltage, check_safety, read_sensor_data
import pytest

def test_raw_to_voltage():
    # Test max value
    assert raw_to_voltage(4096) == 3.3
    # Test 0 value
    assert raw_to_voltage(0) == 0.0
    # Test mid value
    assert raw_to_voltage(2048) == 1.65
    # Test out of range negative value
    assert raw_to_voltage(-10) == 0.0

def test_check_safety():
    # Threshold is 2.5V
    assert check_safety(1.0) == "SAFE"
    assert check_safety(3.0) == "WARNING"
    assert check_safety(2.5001) == "WARNING"

def test_read_sensor_data(tmp_path):
    # Create a dummy CSV file using pytest's tmp_path fixture
    d = tmp_path / "test.csv"
    d.write_text("sensor_id,raw_value\nS1,1024\nS2,2048")
    
    data = read_sensor_data(str(d))
    assert len(data) == 2
    assert data[0]["sensor_id"] == "S1"
    assert data[1]["raw_value"] == "2048"