# Roku-Scanner 1.0.2

Scans LAN for any connected Roku's and returns available device information.

### Prerequisites
* [Python3.X](https://www.python.org/downloads/)
* PIP - should be installed with python, if not [here](https://pip.pypa.io/en/stable/installing/)

## Installation
```shell script
pip3 install roku-scanner
```

## Usage

### CLI
```shell script
python3 -m roku_scanner
```

#### Options
Device data output in JSON.
```shell script
python3 -m roku_scanner --json
```

Increasing timeout on discovery search time. Default is 2 secs. It's advised to use a time less than 10 secs.
```shell script
python3 -m roku_scanner --timeout 5
```

Change search target to target all devices and not only Roku devices. This will result in non roku devices being added to discovery data. As now(1.0.2) only discovery data is returned for non Roku devices.
```shell script
python3 -m roku_scanner --search-target-all
```

Excluding data from output.
```shell script
python3 -m roku_scanner --exclude device-info
```
Exclusion Options
* device-info
* apps
* active-app 
* media-player

### Import Examples

#### Discovery and device data fetching
Discovering Roku's and fetching their device data.
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
Getting device data in JSON.
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
    json_data = roku.as_json()
```

#### XML
Getting device data as XML.
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
    xml_data = roku.as_xml()
```

#### Search Target in Scanner
Changes search target for scanner to search for all devices, this will return Roku devices and any other using [UPnP](https://en.wikipedia.org/wiki/Universal_Plug_and_Play)
```python
from roku_scanner.scanner import Scanner

scanner = Scanner(search_target='upnp:rootdevice')
scanner.discover()
all_types_of_devices = scanner.discovered_devices
```

## Testing

```shell script
pytest tests/
```

## Code Standard
Roku-Scanner follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) standard. 

## Versioning

Roku-Scanner uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/CCecilia/Roku-Scanner/tags).

## Authors

* **Christian Cecilia** - *Initial work*

See also the list of [contributors](https://github.com/CCecilia/Roku-Scanner/graphs/contributors) who participated in this project.
