from pathlib import Path

import pytest

from roku_scanner.custom_types import PathType
from roku_scanner.scanner import Scanner

MOCK_DATA = Path(__file__).parent / 'mock_data'


@pytest.fixture
def discovery_data() -> bytes:
    discovery_data_file: PathType = MOCK_DATA / 'discovery_data.txt'
    with discovery_data_file.open('rb') as f:
        mock_device_data = f.read()

    return mock_device_data


def test_scanner_data_parser(discovery_data: bytes) -> None:
    scanner: Scanner = Scanner()

    parsed: dict = scanner.parse_data(discovery_data)
    expected: dict = {
        'WAKEUP': 'MAC=e6-48-b0-c7-42-5c;Timeout=10',
        'device-group.roku.com': 'DD45456B11E45456E51',
        'LOCATION': 'http://127.0.0.1:8060/',
        'Server': 'Roku/9.2.0 UPnP/1.0 Roku/9.2.0',
        'Ext': '',
        'USN': 'uuid:roku:ecp:YN00XF7876856',
        'ST': 'roku:ecp',
        'Cache-Control': 'max-age=3600'
    }
    assert isinstance(parsed, dict)
    assert parsed.items() == expected.items()


def test_scanner_header_str_to_header_dict():
    mock_header_str: str = 'USN: uuid:roku:ecp:YN00XF7876856'
    parsed: dict = Scanner().header_str_to_header_dict(mock_header_str)
    expected: dict = {
        'USN': 'uuid:roku:ecp:YN00XF7876856'
    }
    assert isinstance(parsed, dict)
    assert parsed.items() == expected.items()
