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
        # type=bool,
        # default=False,
        # required=False,
        help='Search for all devices on network including non-Roku devices.'
    )
    args: ArgList = parser.parse_args()
    timeout: int = args.timeout
    search_target_all: bool = args.search_target_all
    scanner = Scanner(discovery_timeout=timeout)

    if search_target_all:
        scanner.search_target = 'upnp:rootdevice'

    scanner.discover()

    for device in scanner.discovered_devices:
        server: Union[str, None] = device.get('Server', None)
        if server is not None and 'roku' in server.lower():
            roku_location: Union[str, None] = device.get('LOCATION', None)

            if roku_location is not None:
                roku = Roku(location=roku_location, discovery_data=device)
                roku.fetch_data()
                pprint.pprint(roku.as_json(), indent=4)
            else:
                raise Exception('Unable to find LOCATION in device data.')
        else:
            unknown_device = device


if __name__ == "__main__":
    main()
