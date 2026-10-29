import json
import pathlib
import bookmarks_parser

tests_data_path = pathlib.Path(__file__).parent.resolve()
bookmarks_files = ['chrome_bookmarks', 'firefox_bookmarks']
for bookmarks_file in bookmarks_files:
    for parse, suffix in ((bookmarks_parser.parse, ''), (bookmarks_parser.parse_flat, '_flat')):
        bookmarks = parse(tests_data_path / f'{bookmarks_file}.html')
        with open(tests_data_path / f'{bookmarks_file}{suffix}.json', 'w', encoding='utf8') as fp:
            json.dump(bookmarks, fp, indent=2, ensure_ascii=False)
