# Roku-Scanner 1.0.0

Scans LAN for and connected Roku's and returns available device information.

## Installation
```shell script
pip install roku-scanner
```

## Usage

### CLI
```shell script
python -m roku_scanner
```

### Importing
Can used as below.
```python
from roku_scanner.scanner import Scanner
from roku_scanner.roku import Roku

scanner = Scanner()
scanner.discover()

found_devices = scanner.discovered_devices

for device in found_devices:
    roku_location = device.get('LOCATION')
    roku = Roku(location=roku_location, discovery_data=device)
    roku.fetch_data()
    detailed_device_data = roku.data
    print(detailed_device_data)
```

#### JSON
```python
roku_location = device.get('LOCATION')
roku = Roku(location=roku_location, discovery_data=device)
roku.fetch_data()
json_data = roku.as_json()
```

#### XML
```python
roku_location = device.get('LOCATION')
roku = Roku(location=roku_location, discovery_data=device)
roku.fetch_data()
json_data = roku.as_xml()
```



### Options
Device data output to be in JSON.
```shell script
python -m roku_scanner --json
```

Increasing timeout on search time. Default is 2 secs. It advised to use a time less than 10 secs.
```shell script
python -m roku_scanner --timeout 5
```

Change search target to target all devices and not only Roku devices.
```shell script
python -m roku_scanner --search-target-all
```
