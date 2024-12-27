## HTTP Endpoint Health Checker  
 This program monitors the health of HTTP endpoints by periodically testing their availability and logs the cumulative availability percentage for each domain.

## Prerequisites
- Python 3.8 or higher
- `pip` (Python package manager)
- Internet connection for making HTTP requests

## Installation
1. Clone this repository:  
   ```bash
   git clone <repository-url>
   cd <repository-directory> 

## Install the required Python packages
pip install -r requirements.txt

## Configuration File
The program requires a YAML configuration file containing the list of HTTP endpoints to monitor.  
Example which we already created  `endpoints.yml`

## Usage
Run the program by specifying the path to the YAML configuration file:  
```bash
python health_check.py endpoints.yml

## Stopping the Program
To stop the program, press `CTRL+C`.

## Example Output
fetch.com has 33% availability percentage
www.fetchrewards.com has 100% availability percentage







