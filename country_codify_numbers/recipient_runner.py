from typing import Dict, List, Tuple
import csv
import json


def codify_recipient_numbers(dryrun: bool = False) -> int:
    country_to_dial_codes = get_country_to_dial_codes()

    data_file = "test_recipients.csv" if dryrun else "saved_recipient_address.csv"
    data = read_csv_as_list_of_dicts(f"country_codify_numbers/data/{data_file}")
    for row in data:
        for row in data:
            country_code, subscriber_number = infer_country_code_and_sub_number(
                row["contact"], row["country"], country_to_dial_codes
            )
            row["country_code"] = country_code
            row["subscriber_number"] = subscriber_number

    if not dryrun:
        output_sql_to_file(
            data, "country_codify_numbers/results/recipient_address_sql.txt"
        )
    return 0


def get_country_to_dial_codes() -> Dict[str, str]:
    """
    Get a list of country codes from a list of dictionaries.
    """
    with open("country_codify_numbers/data/country_calling_codes.json") as f:
        data = json.load(f)

        ret = {row["isoCode"]: row["dialCode"] for row in data}
        return ret


def read_csv_as_list_of_dicts(filename: str) -> List[Dict[str, str]]:
    """
    Read a CSV file as a list of dictionaries.
    """
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def infer_country_code_and_sub_number(
    phone_number: str, country: str, country_to_dial_codes: Dict[str, str]
) -> Tuple[str, str]:
    """
    Infer the country code and subscriber number
    """
    stripped_phone_number = phone_number
    characters_to_remove = ["+", "-", "(", ")", " ", "\xa0"]
    for character in characters_to_remove:
        stripped_phone_number = stripped_phone_number.replace(character, "")
    stripped_phone_number = stripped_phone_number.lstrip("0")
    if not stripped_phone_number.isnumeric():
        return "", ""

    sub_number = stripped_phone_number
    country_code = f"{country}/{country_to_dial_codes[country]}"

    dialCode = country_to_dial_codes[country].replace("+", "")
    if stripped_phone_number.startswith(dialCode):
        sub_number = stripped_phone_number[len(dialCode) :]

    print(country, phone_number, country_code, sub_number)
    return country_code, sub_number


def output_sql_to_file(data: List[Dict[str, str]], filename: str) -> int:
    """
    Write the SQL values to insert into the database to a file.
    """
    with open(filename, "w") as f:
        for row in data:
            f.write(
                (
                    f"UPDATE <table> SET country_code='{row['country_code']}', "
                    f"subscriber_number='{row['subscriber_number']}' "
                    f"WHERE id='{row['id']}';\n"
                )
            )
    return 1


if __name__ == "__main__":
    codify_recipient_numbers()
