
from collections import abc
from typing import Any, Generator
import warnings


def flatten(seq: Any,
            *,
            flatten_strings: bool = False,
            mapping_action: str = 'drop') -> Generator[Any, None, None]:

    """
    Nested data flattening utility implemented as a generator. Mappings are
    supported.

    :param seq: data to flatten
    :param flatten_strings: whether to flatten strings (bytestrings) as any other sequence
    :param mapping_action: specifies what to do with mappings in the data, allowed values are:
        'drop' - remove mappings from the result,
        'keep' - pass mappings to the result unchanged,
        'flatten_values' - flatten only mappings' values,
        'flatten_items'  - flatten both mappings' keys and values
    :return: generator with flattened data
    """

    # initialize flags by passed mapping action, default action is 'drop'
    keep_mappings, flatten_items, flatten_values = False, False, False
    if mapping_action == 'drop':
        pass
    elif mapping_action == 'keep':
        keep_mappings = True
    elif mapping_action == 'flatten_items':
        flatten_items = True
    elif mapping_action == 'flatten_values':
        flatten_values = True
    # print warning message in case of incorrect mapping action
    else:
        warnings.warn(
            f"unrecognized mapping action '{mapping_action}', "
            f"allowed values are 'drop', 'keep', 'flatten_values', or 'flatten_items'")

    # initial case 1 - seq is not an iterable
    # including a string (bytestring) that can't or snouldn't be flattened
    _do_not_flatten_this_string = (
        isinstance(seq, (str, abc.ByteString)) and
        (len(seq) == 1 or not flatten_strings))
    if not isinstance(seq, abc.Iterable) or _do_not_flatten_this_string:
        yield seq
        return

    # initial case 2 - seq is a mapping
    # it should be passed to flattening, kept as it is, or dropped
    if isinstance(seq, abc.Mapping):
        if flatten_items or flatten_values:
            seq = [seq]
        elif keep_mappings:
            yield seq
            return
        else:
            return

    # general cases
    for subseq in seq:
        # general case 1 - subseq is not an iterable (base case)
        _do_not_flatten_this_string = (
            isinstance(subseq, (str, abc.ByteString)) and
            (len(subseq) == 1 or not flatten_strings))
        if not isinstance(subseq, abc.Iterable) or _do_not_flatten_this_string:
            yield subseq
        # general case 2 - subseq is a mapping (base/recursive case depending on the specified mapping action)
        elif isinstance(subseq, abc.Mapping):
            if flatten_items:
                yield from flatten(subseq.items(), flatten_strings=flatten_strings, mapping_action=mapping_action)
            elif flatten_values:
                yield from flatten(subseq.values(), flatten_strings=flatten_strings, mapping_action=mapping_action)
            elif keep_mappings:
                yield subseq
        # general case 3 - subseq is an iterable (recursive case)
        else:
            yield from flatten(subseq, flatten_strings=flatten_strings, mapping_action=mapping_action)
