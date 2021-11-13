from multidict import MultiDict

def data_to_multidict(dictionary):
    multi = MultiDict()

    key = iter(dictionary)
    values = next(iter(dictionary.values()))

    for value in values:
        multi.add(key=key, value=value)

    return multi
