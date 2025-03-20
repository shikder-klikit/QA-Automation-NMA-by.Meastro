import os
import xml.etree.ElementTree as ET
from datetime import datetime

def parse_maestro_log(log_file):
    """
    Parse a Maestro log file to extract test results.
    Returns a dictionary with test name, status, and message.
    """
    test_name = os.path.basename(log_file).replace(".log", "")
    with open(log_file, "r") as f:
        log_content = f.read()

    # Determine test status based on log content
    if "FAILED" in log_content:
        status = "failed"
        message = "Test failed. Check logs for details."
    elif "PASSED" in log_content:
        status = "passed"
        message = ""
    else:
        status = "skipped"
        message = "Test skipped or incomplete."

    return {
        "name": test_name,
        "status": status,
        "message": message
    }

def convert_maestro_to_junit(maestro_results_dir, output_dir):
    """
    Convert Maestro logs to JUnit XML format.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Create the root element for the JUnit XML
    root = ET.Element("testsuite", name="Maestro Tests", tests="0", failures="0", errors="0", skipped="0", timestamp=datetime.now().isoformat())

    # Process each Maestro log file
    for log_file in os.listdir(maestro_results_dir):
        if log_file.endswith(".log"):
            test_result = parse_maestro_log(os.path.join(maestro_results_dir, log_file))

            # Update test suite statistics
            root.attrib["tests"] = str(int(root.attrib["tests"]) + 1)
            if test_result["status"] == "failed":
                root.attrib["failures"] = str(int(root.attrib["failures"]) + 1)
            elif test_result["status"] == "skipped":
                root.attrib["skipped"] = str(int(root.attrib["skipped"]) + 1)

            # Create a <testcase> element for each test
            testcase = ET.SubElement(root, "testcase", classname="Maestro", name=test_result["name"], time="0.0")

            # Add <failure> or <skipped> elements if applicable
            if test_result["status"] == "failed":
                failure = ET.SubElement(testcase, "failure", message=test_result["message"])
                failure.text = test_result["message"]
            elif test_result["status"] == "skipped":
                skipped = ET.SubElement(testcase, "skipped", message=test_result["message"])
                skipped.text = test_result["message"]

    # Write the JUnit XML file
    tree = ET.ElementTree(root)
    output_file = os.path.join(output_dir, "maestro-results.xml")
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    import sys
    maestro_results_dir = sys.argv[1]
    output_dir = sys.argv[2]
    convert_maestro_to_junit(maestro_results_dir, output_dir)