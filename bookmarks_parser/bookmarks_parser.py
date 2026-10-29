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
    """Parse bookmarks into a flat list; folder titles are in 'path'."""
    def walk(nodes, path):
        for node in nodes:
            if node.get('type') == 'bookmark':
                yield {'path': path, **node}
            elif 'children' in node:
                yield from walk(node['children'], path + [node.get('title', 'untitled')])
    return list(walk(parse(file_path), []))
