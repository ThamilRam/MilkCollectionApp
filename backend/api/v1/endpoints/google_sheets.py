from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.auth import get_current_user
import os
import json
from api.config import settings

router = APIRouter()


def _get_sheets_service():
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except Exception:
        raise RuntimeError('Google API client libraries are required: google-auth, google-api-python-client')

    sa_json = settings.GOOGLE_SERVICE_ACCOUNT_JSON
    if not sa_json:
        raise RuntimeError('Missing GOOGLE_SERVICE_ACCOUNT_JSON environment variable')
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    if sa_json.strip().startswith('{'):
        info = json.loads(sa_json)
        creds = Credentials.from_service_account_info(info, scopes=scopes)
    else:
        creds = Credentials.from_service_account_file(sa_json, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    return service


def _get_next_row(spreadsheet_id: str, sheet_name: str):
    service = _get_sheets_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=sheet_name,
        majorDimension='ROWS'
    ).execute()
    values = result.get('values') or []
    return len(values) + 1


def _append_rows(spreadsheet_id: str, sheet_name: str, rows: List[List]):
    service = _get_sheets_service()
    next_row = _get_next_row(spreadsheet_id, sheet_name)
    body = {'values': rows}
    range_name = f"{sheet_name}!A{next_row}"
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    return result


@router.post('/daily-entries')
def export_daily_entries(entries: List[dict], current_user=Depends(get_current_user)):
    spreadsheet_id = settings.GOOGLE_SHEETS_SPREADSHEET_ID
    if not spreadsheet_id:
        raise HTTPException(status_code=500, detail='GOOGLE_SHEETS_SPREADSHEET_ID not configured')
    rows = []
    for e in entries:
        original_format = "%Y-%m-%d"
        new_date_str = datetime.strptime(e.get('date', ''), original_format).strftime("%d-%m-%Y")
        rows.append([
            new_date_str,
            e.get('session', ''),
            e.get('customer_id', ''),
            e.get('quantity', ''),
            e.get('rate', ''),
            e.get('amount', '')
        ])
    try:
        _append_rows(spreadsheet_id, 'Daily Entry', rows)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {'message': f'Appended {len(rows)} rows to "Daily Entry"'}


@router.post('/payments')
def export_payments(payments: List[dict], current_user=Depends(get_current_user)):
    spreadsheet_id = settings.GOOGLE_SHEETS_SPREADSHEET_ID
    if not spreadsheet_id:
        raise HTTPException(status_code=500, detail='GOOGLE_SHEETS_SPREADSHEET_ID not configured')
    rows = []
    for p in payments:
        original_format = "%Y-%m-%d"
        from_date = datetime.strptime(p.get('from_date', ''), original_format).strftime("%d-%m-%Y")
        end_date = datetime.strptime(p.get('end_date', ''), original_format).strftime("%d-%m-%Y")
        rows.append([
            p.get('customer_id', ''),
            from_date,
            end_date,
            p.get('recorded_amount', ''),
            p.get('status', ''),
            p.get('notes', '')
        ])
    try:
        _append_rows(spreadsheet_id, 'Payments', rows)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return {'message': f'Appended {len(rows)} rows to "Payment Records"'}
