from country_codify_numbers import __version__
from country_codify_numbers.runner import main, read_csv_as_list_of_dicts
from country_codify_numbers.recipient_runner import codify_recipient_numbers


def test_version():
    assert __version__ == "0.1.0"


def test_main():
    assert main(dryrun=True) == 0


def test_read_csv_as_list_of_dicts():
    data = read_csv_as_list_of_dicts("country_codify_numbers/data/test.csv")
    assert data == [
        {"user_id": "2", "meta_value": "123"},
        {"user_id": "5", "meta_value": "456"},
    ]
    assert len(data) == 2


def test_codify_recipient_numbers():
    assert codify_recipient_numbers(dryrun=True) == 0
