import pytest
from src.analytics import validate_readonly_sql

def test_select_sales_allowed():
    assert validate_readonly_sql("SELECT COUNT(*) FROM sales") == "SELECT COUNT(*) FROM sales"

def test_delete_rejected():
    with pytest.raises(ValueError):
        validate_readonly_sql("DELETE FROM sales")

def test_external_file_function_rejected():
    with pytest.raises(ValueError):
        validate_readonly_sql("SELECT * FROM read_csv_auto('secret.csv')")

def test_other_table_rejected():
    with pytest.raises(ValueError):
        validate_readonly_sql("SELECT * FROM customers")
