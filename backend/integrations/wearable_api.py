from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# Environment variables for API keys
FITBIT_CLIENT_ID = os.getenv("FITBIT_CLIENT_ID")
FITBIT_CLIENT_SECRET = os.getenv("FITBIT_CLIENT_SECRET")
GARMIN_CLIENT_ID = os.getenv("GARMIN_CLIENT_ID")
GARMIN_CLIENT_SECRET = os.getenv("GARMIN_CLIENT_SECRET")

@router.get("/fitbit/data")
async def get_fitbit_data(access_token: str):
    try:
        url = "https://api.fitbit.com/1/user/-/activities/date/today.json"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/garmin/data")
async def get_garmin_data(access_token: str):
    try:
        url = "https://api.garmin.com/wellness-api/rest/user/activities"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))