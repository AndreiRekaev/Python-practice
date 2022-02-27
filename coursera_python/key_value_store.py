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
