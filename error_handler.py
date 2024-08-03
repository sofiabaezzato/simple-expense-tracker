class ExpenseTrackerError(Exception):
    """Base class for ExpenseTracker errors"""
    pass

class AuthenticationError(ExpenseTrackerError):
    """Raised when authentication fails"""
    pass

class NoteNotFoundError(ExpenseTrackerError):
    """Raised when the specified note is not found"""
    pass

class SheetNotFoundError(ExpenseTrackerError):
    """Raised when the specified Google Sheet is not found"""
    pass

def display_error_and_exit(error_message):
    print(f"\nError: {error_message}")
    print("Exiting program.")
    exit(1)

def display_warning(warning_message):
    print(f"\nWarning: {warning_message}")