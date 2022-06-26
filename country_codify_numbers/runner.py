import csv
from typing import Dict, Set, Tuple
import json


def main() -> int:
    all_country_codes = get_country_codes()

    data = read_csv_as_list_of_dicts("country_codify_numbers/data/ext_phone.csv")
    for row in data:
        country_code, subscriber_number = infer_country_code_and_sub_number(
            row["meta_value"], list(all_country_codes)
        )
        row["country_code"] = country_code
        row["subscriber_number"] = subscriber_number

    write_to_csv(data, "country_codify_numbers/results/ext_phone_with_country_code.csv")
    return 0


def read_csv_as_list_of_dicts(filename: str) -> list[Dict[str, str]]:
    """
    Read a CSV file as a list of dictionaries.
    """
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def write_to_csv(data: list[Dict[str, str]], filename: str) -> int:
    """
    Write a list of dictionaries to a CSV file.
    """
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return 1


def infer_country_code_and_sub_number(
    phone_number: str, all_country_codes: list[str]
) -> Tuple[str, str]:
    """
    Infer the country code and subscriber number
    """
    characters_to_remove = ["+", "-", "(", ")", " "]
    for character in characters_to_remove:
        phone_number = phone_number.replace(character, "")
    phone_number = phone_number.lstrip("0")
    if not phone_number.isnumeric():
        return "", ""

    country_code = ""
    if len(phone_number) == 8:
        country_code = "65"

    else:
        for code in all_country_codes:
            if phone_number.startswith(code):
                country_code = code
                phone_number = phone_number[len(code) :]
                break

    return country_code, phone_number


def get_country_codes() -> Set[str]:
    """
    Get a list of country codes from a list of dictionaries.
    """
    with open("country_codify_numbers/data/country_calling_codes.json") as f:
        data = json.load(f)

        country_codes = set()
        for row in data:
            country_code = row["dialCode"]
            country_codes.add(country_code.replace("+", ""))
        return country_codes


if __name__ == "__main__":
    main()
