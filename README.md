# IoT Data Validator

#### Video Demo:  <https://youtu.be/_feDPZRA5z8>

## **Definition**

This project is a command-line utility designed to process, convert, and validate raw sensor data logs. It mimics a real-world embedded engineering workflow, where raw ADC (Analog-to-Digital Converter) values must be translated into human-readable voltage levels and checked against safety thresholds.

This tool is specifically useful for debugging firmware logs from microcontrollers like the **RP2040** or **ESP8266**, bridging the gap between low-level hardware data and high-level analysis.

Project structure:

* `project.py`
* `test_project.py`
* `requirements.txt`
* `sensor_data.csv` (Sample Input)
* `README.md`

## **Libraries**

**CSV** : This module implements classes to read and write tabular data in CSV format. It is used here to parse sensor logs and generate reports.

**SYS** : This module is used here for Command Line Arguments processing.

**PYTEST** : The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.

## **Installing Libraries**

There is a `requirements.txt` file that contains the testing library used.
It can be installed by this pip command:

`pip install -r requirements.txt`

## **Usage**

To run the program, you must provide the input CSV file and the desired output CSV file as command-line arguments:

`python project.py input_file.csv output_file.csv`

**Example Execution:**

```bash
$ python project.py sensor_data.csv report.csv
Processing complete. Data written to report.csv

```

**Input File Format (`sensor_data.csv`):**
The input file must contain `sensor_id` and `raw_value` columns.

```csv
sensor_id,raw_value
Temp_01,1024
Batt_01,3500

```

**Generated Output (`report.csv`):**
The program will generate a file containing the converted voltage and safety status.

```csv
sensor_id,voltage,status
Temp_01,0.83,SAFE
Batt_01,2.82,WARNING

```

## **Functioning**

The `project.py` file contains 5 functions including the main function.

### **main()** **function** :

This is the driver function. It verifies that the correct number of command-line arguments are provided. If the command-line arguments are as expected it calls the reader function, iterating through the data to apply conversions and safety checks, and finally calling the writer function to save the results.

### **Core Processing Functions**:

#### **read_sensor_data(filename)** **function** :

This function takes a string argument representing the path to the CSV file. It opens the file and uses `csv.DictReader` to parse the content into a list of dictionaries. It handles `FileNotFoundError` if the input file does not exist.

#### **raw_to_voltage(raw_value)** **function** :

This function performs the mathematical conversion relevant to embedded systems.

* **Input:** An integer representing the raw ADC value (e.g., from a 12-bit ADC like on the RP2040).
* **Logic:** It applies the formula: .
* Resolution is set to **4096** (12-bit).
* Reference Voltage is set to **3.3V**.

The output is calculated using the formula:
```voltage = (raw_Value / 4096) * 3.3```


* **Output:** Returns the calculated voltage as a float.

#### **check_safety(voltage)** **function** :

This function implements the safety logic.

* **Input:** A float representing the voltage.
* **Logic:** It compares the voltage against a defined threshold (2.5V).
* **Output:** Returns a string: `"SAFE"` if the voltage is below the threshold, or `"WARNING"` if it exceeds it.

#### **write_report(filename, data)** **function** :

This function takes the filename for the report and the list of processed dictionaries. It uses `csv.DictWriter` to create a new CSV file with the headers: `sensor_id`, `voltage`, and `status`.

### Author : Pranav Aravindhan V
