import yaml
import json
import ollama
from error_handler import ExpenseTrackerError, display_error_and_exit
from read_keep import read_keep_notes
from write_sheets import write_to_sheet
from halo import Halo

def load_categories():
    with open('categories.yaml', 'r') as file:
        data = yaml.safe_load(file)
    return data['categories']

def load_prompt_template():
    with open('prompt_template.txt', 'r') as file:
        return file.read()

def categorize_expenses(expenses, categories):
    categories_str = "\n".join(f"- {cat['name']}: {cat['description']}" for cat in categories)
    prompt_template = load_prompt_template()
    
    prompt = prompt_template.format(
        expenses=json.dumps(expenses, indent=2),
        categories=categories_str
    )

    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return json.loads(response['message']['content'])

def main():
    spinner = Halo(text='Processing', spinner='dots')
    
    try:
        # Ask for note title before starting the spinner
        note_title = input("Enter the Google Keep note title: ")
        
        spinner.start('Reading notes from Google Keep')
        expenses = read_keep_notes(note_title)
        
        spinner.succeed('Notes read successfully')
        spinner.start('Loading categories')
        categories = load_categories()

        spinner.succeed('Categories loaded')
        spinner.start('Categorizing expenses')
        categorized_expenses = categorize_expenses(expenses, categories)

        spinner.succeed('Expenses categorized')
        # Stop spinner to ask for sheet name
        sheet_name = input("\nEnter the Google Sheets worksheet name: ")
        
        spinner.start('Writing to Google Sheets')
        write_to_sheet(categorized_expenses, sheet_name)

        spinner.succeed("Process completed successfully!")
    except ExpenseTrackerError as e:
        spinner.fail(str(e))
        display_error_and_exit(str(e))
    finally:
        if spinner.spinner_id:
            spinner.stop()

if __name__ == "__main__":
    main()