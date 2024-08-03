# Expense Tracker (from Google Keep to Google Sheets w/AI)
AI-powered Expense Tracker: automates expense tracking by fetching notes from Google Keep, categorizing expenses using AI (Llama 3), and exporting to Google Sheets. Simplify your monthly budgeting with minimal effort!


## How it works

1. Create a new Google Keep note on the first day of the month. Use a consistent naming convention (e.g., "01-january", "02-february").
2. Throughout the month, add your expenses to the note in this format:
    ```
    20 hairdresser
    48 clothes
    10 groceries
    ```
3. At the end of the month, run this script to categorize and export your expenses to Google Sheets.

## Prerequisites

- Python 3.x
- Docker (for obtaining Google tokens)
- Ollama (for automatic expense categorization)

## Setup

1. Clone the repository:
    ```
    git clone https://github.com/sofiabaezzato/simple-expense-tracker.git
    cd expense-tracker
    ```
2. Create and activate a virtual environment:
    - On Windows, in Powershell:
      ```
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```
      python -m venv venv
      source venv/bin/activate
      ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Set up your .env file with the required tokens (see "How to get Google tokens" below).

## How to get Google tokens (for Google Keep Notes)

1. Obtain your Google OAuth token:
    - Visit [this Google page](https://accounts.google.com/v3/signin/identifier?authuser=3&continue=https://accounts.google.com/o/android/auth?lang%3Dit%26cc%26langCountry%3Dit_%26xoauth_display_name%3DAndroid%2BDevice%26tmpl%3Dnew_account%26source%3Dandroid%26return_user_id%3Dtrue&ddm=0&dsh=S-1945412878:1721384156253992&flowName=EmbeddedSetupAndroid#close)
    - Sign in with your Google credentials
    - Click "I agree" when prompted
    - Inspect the page > Application > Cookies > Copy the `oauth` token

2. Use Docker to generate your master token:
    ```
    docker run --rm -it python:3 /bin/bash -c "pip install gpsoauth && python3 -c \"import gpsoauth; print(gpsoauth.exchange_token(input('Email: '), input('OAuth Token: '), input('Android ID: ')))\""
    ```
    - Enter your Google Keep email, OAuth token, and a randomly generated 16-digits hexadecimal Android ID when prompted
    - The resulting `aas_et/` token is your master token

3. Add your Google Keep email and your master token to your .env file:
    ```
    GKEEP_EMAIL=your_oauth_token_here
    MASTER_TOKEN=your_master_token_here
    ```

## Setup Google Sheets API
1. Create a new project in [Google Cloud Console](https://console.cloud.google.com)
2. Enable API and services in the project dashboard
3. Enable Google Sheets API and create credentials (make sure to grant Editor access to the account)
4. Create and download the keys file
5. Import the keys file in your project folder and name it `g-sheets-credentials.json`
6. Share the Google Sheet with the Service Account previously created
7. **Add the sheet id (`SHEET_ID`) you want to write on in the `.env` file**


## Install Ollama

1. Install [Ollama](https://ollama.ai/download)
2. Pull the Llama 3 model: `ollama pull llama3`
3. Start the Ollama service: `ollama serve`

## Usage

1. Ensure your virtual environment is activated
2. Make a copy of the `TEMPLATE` sheet in your worksheet and give it the name of the month as a title
2. Run the script: `python init.py`
3. Enter the title of your Google Keep note and the title of the sheet when prompted

**Note: you can also run `read_keep.py` and `write_sheets.py` individually for testing purposes.**

## Customization

You can customize expense categories by editing the `categories.yaml` file in the project root. You can also edit the AI prompt in the `prompt_template.txt` file.

## Troubleshooting

If you encounter any issues, please check the following:
- Ensure all tokens in your .env file are correct and up to date. Your `env` file should look like this:
    ```
    MASTER_TOKEN=<your master token>
    GKEEP_EMAIL=<your Google Keep email>
    SHEET_ID=<id of your Google Sheet>
- Verify that Ollama is running and the Llama3 model is installed

For further assistance, please open an issue on the GitHub repository.

## Contributing

Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.