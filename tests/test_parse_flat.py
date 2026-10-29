import json
import os

import pytest
import bookmarks_parser

tests_data_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests_data'))


@pytest.mark.parametrize("input_path, result_path", [('chrome_bookmarks.html', 'chrome_bookmarks_flat.json'),
                                                     ('firefox_bookmarks.html', 'firefox_bookmarks_flat.json')])
def test_parser(input_path, result_path):
    input_path = os.path.join(tests_data_path, input_path)
    result_path = os.path.join(tests_data_path, result_path)
    with open(result_path, 'r') as f:
        result = json.load(f)
    assert bookmarks_parser.parse_flat(input_path) == result
