# flatten
Nested data flattening utility implemented as a generator. Mappings are supported.

### 1. Basic example
Usage is pretty straightforward. Just remember that the result is a generator.
```
>>> x = [1, 2, 3, (4, 5, [6], (7,)), 8, 9]
>>> list(flatten(x))
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### 2. Strings
By default strings are treated as values. Also strings may be flattened into characters like any other iterable.
```
>>> x = (('qwe', 'rty'), ('asd',), ('zxc'))
>>> list(flatten(x))
['qwe', 'rty', 'asd', 'zxc']
>>> list(flatten(x, flatten_strings=True))
['q', 'w', 'e', 'r', 't', 'y', 'a', 's', 'd', 'z', 'x', 'c']
```

### 3. Mappings
By default mappings are removed from the result. However, mappings may be processed in four different manners: `drop` - remove mappings from the result, `keep` - pass mappings to the result unchanged, `flatten_values` - flatten only mappings' values, `flatten_items` - flatten both mappings' keys and values.
```
>>> x = {1: 'qwe', 2: [{'a': ('asd', 'asdf')}, 'zxc']}
>>> list(flatten(x, mapping_action='drop'))
[]
>>> list(flatten(x, mapping_action='keep'))
[{1: 'qwe', 2: [{'a': ('asd', 'asdf')}, 'zxc']}]
>>> list(flatten(x, mapping_action='flatten_values'))
['qwe', 'asd', 'asdf', 'zxc']
>>> list(flatten(x, mapping_action='flatten_items'))
[1, 'qwe', 2, 'a', 'asd', 'asdf', 'zxc']
>>> list(flatten(x, mapping_action='flatten_items', flatten_strings=True))
[1, 'q', 'w', 'e', 2, 'a', 'a', 's', 'd', 'a', 's', 'd', 'f', 'z', 'x', 'c']
```

```
>>> x = [
...     'Andrew',
...     'Mary',
...     {'name': 'Carl'},
...     {'name': 'Harry'},
...     {'group_1': ['Alex', 'John'], 'group_2': [{'name': 'Lisa'}, {'name': 'Bob'}]}]
>>> list(flatten(x, mapping_action='flatten_values'))
['Andrew', 'Mary', 'Carl', 'Harry', 'Alex', 'John', 'Lisa', 'Bob']
```

### 4. More
Works with generators and custom types that support [python collections ABCs' interfaces](https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes) (Iterable, Mapping).

### 5. Even more
Never actually tested with real-world strings (emojis, encodings, languages, etc). Never tested in asynchronous code.
