import argparse
import pprint
from typing import Union

from roku_scanner.custom_types import ArgList, ArgParser
from roku_scanner.roku import Roku
from roku_scanner.scanner import Scanner


def main() -> None:
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
        help='return results as json.'
    )
    args: ArgList = parser.parse_args()
    timeout: int = args.timeout
    search_target_all: bool = args.search_target_all
    as_json: bool = args.json
    scanner = Scanner(discovery_timeout=timeout)

    if search_target_all:
        scanner.search_target = 'upnp:rootdevice'

    scanner.discover()

    if as_json:
        data: str = ''
    else:
        data: str = f'<?xml version="1.0" encoding="UTF-8" ?>\n'

    for device in scanner.discovered_devices:
        server: Union[str, None] = device.get('Server', None)
        if server is not None and 'roku' in server.lower():
            roku_location: Union[str, None] = device.get('LOCATION', None)

            if roku_location is not None:
                roku = Roku(location=roku_location, discovery_data=device)
                roku.fetch_data()

                if as_json:
                    data += roku.as_json()
                else:
                    data += roku.as_xml()
            else:
                raise Exception('Unable to find LOCATION in device data.')
        else:
            unknown_device = device

    # pprint.pprint(data)
    print(data)


if __name__ == "__main__":
    main()
