import requests
import yaml
import time
import threading
from collections import defaultdict

# Function to check if the HTTP request was successful (UP)
def check_health(endpoint): 
    try:
        method = endpoint.get("method", "GET").upper()
        url = endpoint["url"]
        headers = endpoint.get("headers", {})
        body = endpoint.get("body", None)  

        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, headers=headers, data=body, timeout=5)
        else:
            response = None

        # Check if response code is 2xx and latency is under 500ms
        if response and 200 <= response.status_code < 300 and response.elapsed.total_seconds() * 1000 < 500:
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Function to parse YAML file and return the list of endpoints
def parse_yaml(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

# Function to log the availability percentage for each domain
def log_availability(domain_stats):
    for domain, stats in domain_stats.items():
        if stats["total"] > 0:
            availability = round(100 * (stats["up"] / stats["total"]))
            print(f"{domain} has {availability}% availability percentage")

# Function to monitor health of all endpoints
def monitor_health(endpoints, domain_stats):
    while True:
        for endpoint in endpoints:
            result = check_health(endpoint)
            url = endpoint["url"]
            domain = url.split("/")[2]  # Extract domain from URL

            if result == "UP":
                domain_stats[domain]["up"] += 1
            domain_stats[domain]["total"] += 1

        # Log the current availability percentage for each domain
        log_availability(domain_stats)
        time.sleep(15)

# Main function to start the program
def main(file_path):
    # Parse the YAML configuration file
    endpoints = parse_yaml(file_path)

    # Dictionary to keep track of the availability stats for each domain
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    # Start the health monitoring in a separate thread
    monitoring_thread = threading.Thread(target=monitor_health, args=(endpoints, domain_stats))
    monitoring_thread.daemon = True  # Run the thread in the background
    monitoring_thread.start()

    # Run indefinitely until the user interrupts (CTRL+C)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting program...")
        monitoring_thread.join()

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python monitor.py <yaml_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    main(config_file)





