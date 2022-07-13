from typing import Dict, List, Tuple
import csv
import json


def main(dryrun: bool = False) -> int:
    iso_and_dial_codes = get_iso_and_dial_codes()

    data_file = "test.csv" if dryrun else "ext_phone.csv"
    data = read_csv_as_list_of_dicts(f"country_codify_numbers/data/{data_file}")
    for row in data:
        country_code, subscriber_number = infer_country_code_and_sub_number(
            row["meta_value"], list(iso_and_dial_codes)
        )
        row["country_code"] = country_code
        row["subscriber_number"] = subscriber_number

    if not dryrun:
        output_sql_to_file(data, "country_codify_numbers/results/usermeta_sql.txt")
    return 0


def read_csv_as_list_of_dicts(filename: str) -> List[Dict[str, str]]:
    """
    Read a CSV file as a list of dictionaries.
    """
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


def output_sql_to_file(data: List[Dict[str, str]], filename: str) -> int:
    """
    Write the SQL values to insert into the database to a file.
    """
    with open(filename, "w") as f:
        f.write("INSERT IGNORE INTO <table> (user_id, meta_key, meta_value) VALUES\n")
        for row in data:
            f.write(
                (
                    f"('{row['user_id']}', 'subscriber_number', "
                    f"'{row['subscriber_number']}'),\n"
                )
            )
            f.write(f"('{row['user_id']}', 'country_code', '{row['country_code']}'),\n")
    return 1


def infer_country_code_and_sub_number(
    phone_number: str, iso_and_dial_codes: List[str]
) -> Tuple[str, str]:
    """
    Infer the country code and subscriber number
    """
    characters_to_remove = ["+", "-", "(", ")", " ", "\xa0"]
    for character in characters_to_remove:
        phone_number = phone_number.replace(character, "")
    phone_number = phone_number.lstrip("0")
    if not phone_number.isnumeric():
        return "", ""

    country_code = ""
    sub_number = ""
    if len(phone_number) == 8:
        country_code = "SG/+65"
        sub_number = phone_number

    else:
        for iso_and_dial_code in iso_and_dial_codes:
            dialCode = iso_and_dial_code.split("/")[1].replace("+", "")
            if phone_number.startswith(dialCode):
                country_code = iso_and_dial_code
                sub_number = phone_number[len(dialCode) :]
                if iso_and_dial_code == "AU/+61":
                    break

    return country_code, sub_number


def get_iso_and_dial_codes() -> List[str]:
    """
    Get a list of country codes from a list of dictionaries.
    """
    with open("country_codify_numbers/data/country_calling_codes.json") as f:
        data = json.load(f)

        country_codes = [f"{row['isoCode']}/{row['dialCode']}" for row in data]
        country_codes.sort()
        return country_codes


if __name__ == "__main__":
    main()
