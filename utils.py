
from collections import defaultdict


def reverse_nested_dict(data_dict):
    """
    {(outerKey, innerKey): values for outerKey, innerDict in item_dict['val'].items() for
              innerKey, values in innerDict.items()}
    """
    flipped = defaultdict(dict)
    for key, val in data_dict.items():
        for subkey, subval in val.items():
            flipped[subkey][key] = subval
    return dict(flipped)
