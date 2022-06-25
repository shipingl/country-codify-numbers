from country_codify_numbers import __version__
from country_codify_numbers.runner import main, read_csv_as_list_of_dicts


def test_version():
    assert __version__ == "0.1.0"


def test_main():
    assert main() == 0


def test_read_csv_as_list_of_dicts():
    data = read_csv_as_list_of_dicts("country_codify_numbers/data/test.csv")
    assert data == [
        {"umeta_id": "1", "user_id": "2", "meta_key": "ext_phone", "meta_value": "123"},
        {"umeta_id": "4", "user_id": "5", "meta_key": "ext_phone", "meta_value": "456"},
    ]
    assert len(data) == 2
