import os
import tempfile
import argparse
import json


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Process some key or values.')
    parser.add_argument('--key', help="key")
    parser.add_argument('--val', default=None, help="value")

    args = parser.parse_args()

    our_key = args.key
    our_value = args.val

    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

    if os.path.exists(storage_path):
        with open(storage_path) as f:

            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                data = {}

    else:
        with open(storage_path,'w') as f:
            data = {}



    if our_value:
        data.setdefault(our_key, []).append(our_value)
        with open(storage_path, 'w') as f:
            json.dump(data, f)

    else:
        result = ', '.join(data.get(our_key, ''))

        print(result or None)

###### Coursera solution

import argparse
import json
import os
import tempfile


def read_data(storage_path):
    if not os.path.exists(storage_path):
        return {}

    with open(storage_path, 'r') as file:
        raw_data = file.read()
        if raw_data:
            return json.loads(raw_data)
        return {}


def write_data(storage_path, data):
    with open(storage_path, 'w') as f:
        f.write(json.dumps(data))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='Key')
    parser.add_argument('--val', help='Value')
    return parser.parse_args()


def put(storage_path, key, value):
    data = read_data(storage_path)
    data[key] = data.get(key, list())
    data[key].append(value)
    write_data(storage_path, data)


def get(storage_path, key):
    data = read_data(storage_path)
    return data.get(key, [])


def main(storage_path):
    args = parse()

    if args.key and args.val:
        put(storage_path, args.key, args.val)
    elif args.key:
        print(*get(storage_path, args.key), sep=', ')
    else:
        print('The program is called with invalid parameters.')


if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    main(storage_path)
