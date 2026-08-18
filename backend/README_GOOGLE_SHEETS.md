To enable Google Sheets export endpoints, install required packages into the backend virtual environment:

pip install google-api-python-client google-auth google-auth-httplib2

Configuration (environment variables):
- `GOOGLE_SERVICE_ACCOUNT_JSON` : Either the full service account JSON (escaped) or a path to the JSON file on disk.
- `GOOGLE_SHEETS_SPREADSHEET_ID` : The target spreadsheet ID.

The API exposes these endpoints (requires authentication):
- POST /api/v1/export/daily-entries  -> body: list of {date, session, customer_id, quantity, rate, amount}
- POST /api/v1/export/payments      -> body: list of {customer_id, from_date, end_date, recorded_amount, status, notes}

These endpoints will append rows to the "Daily Entry" and "Payment Records" sheets respectively.
