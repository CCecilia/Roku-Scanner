# coding=utf-8
"""
Usage:
    python3 -m roku_scanner

CLI-Args:
    --timeout, -t :: Timeout for each device discovery query
    --search-target-all, -s :: Search for all devices on network including non-Roku devices
    --json :: Returns results as json. Default format is xml.
    --exclude :: Excludes certain ECP data from the output.

ToDos:
    1. find something to do with non roku devices, could be useful?
"""
import argparse
import pprint

from typing import List, Union

from roku_scanner.custom_types import ArgList, ArgParser
from roku_scanner.roku import Roku
from roku_scanner.scanner import Scanner


def main() -> None:
    """
    Handle cli usage/args of roku scanner
    """
    parser: ArgParser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--timeout',
        type=int,
        default=2,
        required=False,
        help='Timeout for each device discovery query?'
    )
    parser.add_argument(
        '-s',
        '--search-target-all',
        action='store_true',
        help='Search for all devices on network including non-Roku devices.'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Returns results as json.'
    )
    parser.add_argument(
        '--exclude',
        choices=['device-info', 'apps', 'active-app', 'media-player'],
        nargs='+',
        help='Data to exclude from output.'
    )
    args: ArgList = parser.parse_args()
    output_exclusions: List[str] = args.exclude
    if output_exclusions is not None:
        output_exclusions = list(map(lambda x: x.replace('-', '_'), output_exclusions))

    timeout: int = args.timeout
    search_target_all: bool = args.search_target_all
    as_json: bool = args.json
    scanner = Scanner(discovery_timeout=timeout)

    if search_target_all:
        scanner.search_target = 'upnp:rootdevice'

    scanner.discover()

    found_data: str = f'<?xml version="1.0" encoding="UTF-8" ?>\n'

    if as_json:
        found_data = ''

    for device in scanner.discovered_devices:
        server: Union[str, None] = device.get('Server', None)
        if server is not None and 'roku' in server.lower():
            roku_location: Union[str, None] = device.get('LOCATION', None)

            if roku_location is not None:
                roku = Roku(location=roku_location, discovery_data=device)
                roku.fetch_data()

                if as_json:
                    found_data += roku.as_json(output_exclusions)
                else:
                    found_data += roku.as_xml(output_exclusions)
            else:
                raise Exception('Unable to find LOCATION in device data.')
        else:
            unknown_device = device

    if as_json:
        pprint.pprint(found_data, indent=4)
    else:
        print(found_data)


if __name__ == "__main__":
    main()
