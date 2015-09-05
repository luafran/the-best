_items = {
    'car': 'fiat 128',
    'wine': 'toro',
    'beer': 'imperial',
    'movie': 'back to the future'
}

def get_items():
    return _items.keys()
    
def get_item_answer(item):
    return _items[item]

