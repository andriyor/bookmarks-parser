from bs4 import BeautifulSoup


def get_node_data(node):
    data = {}
    for child in node:
        if child.name == 'a':
            data['type'] = 'bookmark'
            data['url'] = child.get('href')
            data['title'] = child.text
            data['add_date'] = child.get('add_date')
            data['icon'] = child.get('icon')
            # only in FF
            icon_uri = child.get('icon_uri')
            if icon_uri:
                data['icon_uri'] = icon_uri
            tags = child.get('tags')
            if tags:
                data['tags'] = tags.split(',')
        elif child.name == 'h3':
            data['type'] = 'folder'
            data['title'] = child.text
            data['add_date'] = child.get('add_date')
            data['last_modified'] = child.get('last_modified')

            data['ns_root'] = None
            # for Bookmarks Toolbar in FF and Bookmarks bar in Chrome
            if child.get('personal_toolbar_folder'):
                data['ns_root'] = 'toolbar'
            # FF Other Bookmarks
            if child.get('unfiled_bookmarks_folder'):
                data['ns_root'] = 'other_bookmarks'
        elif child.name == 'dl':
            # store DL element reference for further processing the child nodes
            data['__dir_dl'] = child

    if data['type'] == 'folder' and not data.get('__dir_dl'):
        if node.next_sibling and node.next_sibling.name == "dd":
            dls = node.next_sibling.find_all('dl')
            if dls:
                data['__dir_dl'] = dls[0]
    return data


def process_dir(bookmark_dir, level):
    items = []
    menu_root = None
    for child in bookmark_dir:
        if child.name != 'dt':
            continue
        item_data = get_node_data(child)
        if level == 0 and (not item_data.get('ns_root')):
            if menu_root is None:
                # For chrome
                if child.previous_sibling.name == "dt":
                    menu_root = {'title': "Other bookmarks", 'children': [], 'ns_root': 'menu'}
                # for FF
                else:
                    menu_root = {'title': "Bookmarks Menu", 'children': [], 'ns_root': 'menu'}
            if item_data.get('__dir_dl'):
                item_data['children'] = process_dir(item_data['__dir_dl'], level + 1)
                del item_data['__dir_dl']
            menu_root['children'].append(item_data)
        else:
            if item_data.get('__dir_dl'):
                item_data['children'] = process_dir(item_data['__dir_dl'], level + 1)
                del item_data['__dir_dl']
            items.append(item_data)
    if menu_root:
        items.append(menu_root)
    return items


def parse(file_path):
    with open(file_path, 'rb') as f:
        soup = BeautifulSoup(f, "html5lib")
    dls = soup.find_all('dl')
    bookmarks = process_dir(dls[0], 0)
    return bookmarks

def parse_flat(file_path):
    """Parse bookmarks into a list without nesting. The directory path can be found in 'path'. """
    bookmarks = parse(file_path=file_path)
    current_dir = []
    bookmarks_flat = []

    # define a recursive function which will load bookmarks_flat
    def recursive_flat_parse(bookmarks, current_dir):

        # the node has children
        if isinstance(bookmarks, dict) and 'children' in bookmarks:
            for child in bookmarks['children']:
                recursive_flat_parse(child, current_dir + [bookmarks.get('title', 'untitled')])

        # the node is a bookmark
        if isinstance(bookmarks, dict) and 'type' in bookmarks and bookmarks['type'] == 'bookmark':
            # add a new tag called 'path' which contains the titles from the directory path
            new_bookmark = {'path':current_dir}
            new_bookmark.update(bookmarks)
            bookmarks_flat.append(new_bookmark)
        
        # the node is not a node, but a list (outermost element usually)
        if isinstance(bookmarks, list):
            for child in bookmarks:
                recursive_flat_parse(child, current_dir)
    
    # actually load bookmarks_flat
    recursive_flat_parse(bookmarks=bookmarks, current_dir=current_dir)

    return bookmarks_flat
