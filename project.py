import sys
import csv
from typing import List, Dict

# Constants for simulation (e.g., 12-bit ADC on an RP2040)
ADC_RESOLUTION = 4096 
V_REF = 3.3
SAFE_VOLTAGE_MAX = 2.5

def main():
    if len(sys.argv) < 3:
        sys.exit("Usage: python project.py <input.csv> <output.csv>")

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # 1. Read the data
    try:
        data = read_sensor_data(input_file)
    except FileNotFoundError:
        sys.exit("Input file not found.")

    processed_data = []
    
    # 2. Process each row
    for row in data:
        raw_val = int(row["raw_value"])
        
        # Function 2: Convert
        voltage = raw_to_voltage(raw_val)
        
        # Function 3: Validate
        status = check_safety(voltage)
        
        processed_data.append({
            "sensor_id": row["sensor_id"],
            "voltage": round(voltage, 2),
            "status": status
        })

    # 3. Write results
    write_report(output_file, processed_data)
    print(f"Processing complete. Data written to {output_file}")


def read_sensor_data(filename: str) -> List[Dict[str, str]]:
    """
    Reads a CSV file and returns a list of dictionaries.
    Expected CSV columns: sensor_id, raw_value
    """
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def raw_to_voltage(raw_value: int) -> float:
    """
    Converts a raw ADC value (0-4095) to Voltage (0-3.3V).
    Formula: (raw / resolution) * reference_voltage
    """
    if raw_value < 0:
        return 0.0
    return (raw_value / ADC_RESOLUTION) * V_REF


def check_safety(voltage: float) -> str:
    """
    Returns 'SAFE' if voltage is below threshold, else 'WARNING'.
    """
    if voltage > SAFE_VOLTAGE_MAX:
        return "WARNING"
    return "SAFE"


def write_report(filename: str, data: List[Dict]):
    """
    Writes the processed data to a new CSV file.
    """
    fieldnames = ["sensor_id", "voltage", "status"]
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    main()