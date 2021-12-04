from multidict import MultiDict

def data_to_multidict(dictionary):
    multi = MultiDict()

    key = iter(dictionary)
    values = next(iter(dictionary.values()))

    for value in values:
        multi.add(key=key, value=value)

    return multi

def split_bulk(bulk: list):
    # Split bulk in groups of 150
    split = 150  
    split_points = [i for i in range(0, len(bulk), split)]
    split_groups = [bulk[ind:ind + split] for ind in split_points]

    return split_groups
