ITEMS = {
    'car': 'fiat 128',
    'wine': 'toro',
    'beer': 'imperial',
    'movie': 'back to the future'
}


def get_items():
    return ITEMS.keys()


def get_item_answer(item):
    return ITEMS[item]
