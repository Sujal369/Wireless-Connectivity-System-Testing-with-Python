import logging
import csv
import asyncio
from ping3 import ping, verbose_ping
from bleak import BleakScanner

# Configure logging
logging.basicConfig(
    filename="system_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler())

# List to store test results
test_results = []

# Wi-Fi Connectivity Test
def test_wifi_connectivity():
    logging.info("Starting Wi-Fi connectivity test.")
    try:
        response = ping("8.8.8.8")  # Ping Google's public DNS server
        if response:
            logging.info(f"Wi-Fi test passed. Ping response: {response} ms")
            test_results.append(
                {"Test": "Wi-Fi Connectivity", "Status": "Pass", "Details": f"Ping response: {response} ms"}
            )
        else:
            raise Exception("No response from server.")
    except Exception as e:
        logging.error(f"Wi-Fi test failed: {e}")
        test_results.append(
            {"Test": "Wi-Fi Connectivity", "Status": "Fail", "Details": str(e)}
        )

# Bluetooth Discovery Test
async def test_bluetooth_discovery():
    logging.info("Starting Bluetooth discovery test.")
    try:
        devices = await BleakScanner.discover()
        if devices:
            device_names = [(d.name, d.address) for d in devices]
            logging.info(f"Bluetooth test passed. Found devices: {device_names}")
            test_results.append(
                {"Test": "Bluetooth Discovery", "Status": "Pass", "Details": f"Devices: {device_names}"}
            )
        else:
            raise Exception("No devices found.")
    except Exception as e:
        logging.error(f"Bluetooth test failed: {e}")
        test_results.append(
            {"Test": "Bluetooth Discovery", "Status": "Fail", "Details": str(e)}
        )

# Simultaneous Operations Test
def test_simultaneous_operations():
    logging.info("Starting simultaneous operations test.")
    try:
        for i in range(3):  # Simulate multiple operations
            response = ping("8.8.8.8")
            if response:
                logging.info(f"Operation {i + 1}: Ping response: {response} ms")
            else:
                raise Exception("Operation failed during simultaneous execution.")
        logging.info("Simultaneous operations test passed.")
        test_results.append(
            {"Test": "Simultaneous Operations", "Status": "Pass", "Details": "All operations executed successfully."}
        )
    except Exception as e:
        logging.error(f"Simultaneous operations test failed: {e}")
        test_results.append(
            {"Test": "Simultaneous Operations", "Status": "Fail", "Details": str(e)}
        )

# Generate Test Report
def generate_report():
    logging.info("Generating test report.")
    with open("test_report.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["Test", "Status", "Details"])
        writer.writeheader()
        writer.writerows(test_results)
    logging.info("Test report generated: test_report.csv")

# Main Execution
if __name__ == "__main__":
    logging.info("Starting system testing.")
    test_wifi_connectivity()
    asyncio.run(test_bluetooth_discovery())  # Run Bluetooth discovery asynchronously
    test_simultaneous_operations()
    generate_report()
    logging.info("System testing completed. Check 'test_report.csv' and logs for details.")
