import argparse
import json
from pathlib import Path


def generate_diff(first_file: str, second_file: str) -> str:
    """Checks files for difference and convergence

    Args:
        first_file (str): [Path to first file]
        second_file (str): [Path to second file]

    Returns:
        str: [Difference]
    """
    first_file = Path(first_file)
    second_file = Path(second_file)

    with first_file.open() as f:
        first_data = json.load(f)

    with second_file.open() as f:
        second_data = json.load(f)

    union_keys = sorted(first_data.keys() | second_data.keys())

    diff = []
    diff.append('{')
    for key in union_keys:
        val1 = first_data.get(key, 'no_val_1')
        val2 = second_data.get(key, 'no_val_2')

        if val1 == val2:
            diff.append(f'    {key}: {val1}')
        elif val1 == 'no_val_1':
            diff.append(f'  + {key}: {val2}')
        elif val2 == 'no_val_2':
            diff.append(f'  - {key}: {val1}')
        elif val1 != val2:
            diff.append(f'  - {key}: {val1}')
            diff.append(f'  + {key}: {val2}')
    diff.append('}')

    return "\n".join(diff)


def main():
    parser = argparse.ArgumentParser(description='Generate diff')
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument("-f", "--format", help="set format of output")
    args = parser.parse_args()
    diff = generate_diff(args.first_file, args.second_file)
    print(diff)


if __name__ == '__main__':
    main()
