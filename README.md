# bookmarks-parser
[![Build Status](https://travis-ci.org/andriyor/bookmarks-parser.svg?branch=master)](https://travis-ci.org/andriyor/bookmarks-parser)
[![codecov](https://codecov.io/gh/andriyor/bookmarks-parser/branch/master/graph/badge.svg)](https://codecov.io/gh/andriyor/bookmarks-parser)
[![image](https://img.shields.io/pypi/v/bookmarks-parser.svg)](https://pypi.org/project/bookmarks-parser/)
[![image](https://img.shields.io/pypi/l/bookmarks-parser.svg)](https://pypi.org/project/bookmarks-parser/)
[![image](https://img.shields.io/pypi/pyversions/bookmarks-parser.svg)](https://pypi.org/project/bookmarks-parser/)

Parsing Netscape bookmark (Google Chrome, Firefox, ... export files) .

## Installation
```
$ pip install bookmarks-parser
```

## Usage
### `parse` Usage
The function `parse` returns a list of nested dicts representing the directory structure of your bookmarks file. 
```python
import pprint
import bookmarks_parser

bookmarks = bookmarks_parser.parse("bookmarks.html")
pprint.pprint(bookmarks)
```
### `parse` Output Examples
+ [Firefox](/tests/tests_data/firefox_bookmarks.json)
+ [Chrome](/tests/tests_data/chrome_bookmarks.json)

### `parse_flat` Usage
The function `parse_flat` returns all bookmarks in a single, non-nested list.
```python
import pprint
import bookmarks_parser

bookmarks = bookmarks_parser.parse_flat("bookmarks.html")
pprint.pprint(bookmarks)
```
### `parse_flat` Output Examples
+ [Firefox](/tests/tests_data/firefox_bookmarks_flat.json)
+ [Chrome](/tests/tests_data/chrome_bookmarks_flat.json)

## Development
Install [Poetry](https://poetry.eustace.io/docs/)   
```
$ poetry install
```
run tests
```
$ poetry run pytest --cov=bookmarks_parser
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
