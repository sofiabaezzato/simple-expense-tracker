import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os
from error_handler import ExpenseTrackerError, SheetNotFoundError, display_error_and_exit

def prepare_data_for_sheets(data):
    if not data or not isinstance(data, list):
        raise ValueError("Data must be a non-empty list")

    if not all(isinstance(row, list) and len(row) == 3 for row in data):
        raise ValueError("Each row must be a list with exactly 3 elements")

    prepared_data = []
    for row in data:
        item, category, amount = row
        prepared_data.append([str(item), str(category), float(amount)])

    return prepared_data

def write_to_sheet(values, sheet_name):
    load_dotenv()

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_file("g-sheets-credentials.json", scopes=SCOPES)
    client = gspread.authorize(credentials)

    sheet_id = os.getenv("SHEET_ID")

    if not sheet_id:
        raise display_error_and_exit("No sheet ID found in the .env file")

    try:
        prepared_values = prepare_data_for_sheets(values)

        worksheet = client.open_by_key(sheet_id)
        selected_sheet = worksheet.worksheet(sheet_name)
        
        if selected_sheet.row_count == 0:
            headers = ["Item", "Category", "Amount"]
            selected_sheet.append_row(headers)

        # Where to write in the Sheet file
        selected_sheet.update(prepared_values, f"A2:C{len(prepared_values) + 1}")
        print(f"\nSuccessfully added {len(prepared_values)} rows to the sheet '{sheet_name}'.")

    except gspread.exceptions.APIError as e:
        raise ExpenseTrackerError(f"An API error occurred: {e}")
    except gspread.exceptions.WorksheetNotFound:
        raise SheetNotFoundError(f"Worksheet '{sheet_name}' not found. Please check the sheet name.")
    except ValueError as e:
        raise ExpenseTrackerError(f"Data format error: {e}")
    except Exception as e:
        raise ExpenseTrackerError(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Test data
    try:
        test_values = [
            ["spesa", "Grocery + Essentials", 20],
            ["spesa", "Grocery + Essentials", 40],
            ["spesa", "Grocery + Essentials", 50]
        ]
        write_to_sheet(test_values, sheet_name='Test')
    except ExpenseTrackerError as e:
        display_error_and_exit(str(e))