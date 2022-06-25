import csv
from typing import Dict


def main() -> int:
    data = read_csv_as_list_of_dicts("country_codify_numbers/data/ext_phone.csv")
    print(data)
    return 0


def read_csv_as_list_of_dicts(filename: str) -> list[Dict[str, str]]:
    """
    Read a CSV file as a list of dictionaries.
    """
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


if __name__ == "__main__":
    main()
