# Roku-Scanner 1.0.0

Scans LAN for and connected Roku's and returns available device information.

## Installation
```shell script
pip install roku
```

## Usage

Normal usage.
```shell script
python -m roku_scanner
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
