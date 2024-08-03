import gkeepapi
import logging
import sys
import re
import os
from dotenv import load_dotenv
from error_handler import AuthenticationError, ExpenseTrackerError, NoteNotFoundError, display_error_and_exit, display_warning

def setup_logging():
    logger = logging.getLogger("gkeepapi")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def authenticate_keep():
    load_dotenv()
    master_token = os.getenv('MASTER_TOKEN')
    gkeep_email = os.getenv('GKEEP_EMAIL')
    keep = gkeepapi.Keep()
    if gkeep_email and master_token:
        try:
            keep.authenticate(gkeep_email, master_token)
            print(f"\nSuccessfully authenticated as {gkeep_email}")
            return keep
        except Exception as e:
            raise AuthenticationError(f"Authentication failed: {str(e)}")
    else:
        raise AuthenticationError("No Google Keep user email (GKEEP_EMAIL) or MASTER_TOKEN found in .env file")

def get_expenses_from_note(keep, note_title):
    try:
        notes = keep.find(query=note_title)
        matching_notes = list(notes)
        
        if not matching_notes:
            raise NoteNotFoundError(f"No note found with the title: {note_title}")

        expenses = []
        invalid_lines = []
        for note in matching_notes:
            print(f"\nProcessing note: {note.title}")
            for line_number, line in enumerate(note.text.split('\n'), 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                match = re.match(r'^(\d+)\s+(.+)$', line)
                if match:
                    amount, description = match.groups()
                    expenses.append({"amount": int(amount), "description": description.strip()})
                else:
                    invalid_lines.append((line_number, line))
        
        print(f"\nFound {len(expenses)} valid expenses in the note.")
        if invalid_lines:
            display_warning("The following lines were not in the correct format and were skipped:")
            for line_number, line in invalid_lines:
                print(f"  Line {line_number}: {line}")
            print("Correct format is: <amount> <description>, e.g., '20 hairdresser'")
        
        return expenses
    except Exception as e:
        raise ExpenseTrackerError(f"Error processing note: {str(e)}")

def read_keep_notes(note_title):
    logger = setup_logging()
    keep = authenticate_keep()
    return get_expenses_from_note(keep, note_title)

if __name__ == "__main__":
    note_title = input("Enter the Google Keep note title: ")
    try:
        expenses = read_keep_notes(note_title)
        print(f"\nExpenses found: {expenses}")
    except ExpenseTrackerError as e:
        display_error_and_exit(str(e))