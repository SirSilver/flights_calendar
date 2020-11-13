from aiohttp import ClientSession
from asyncio import sleep
from datetime import date, timedelta


async def fetch_flights(fly_from, fly_to, date_from, date_to):
    """
    Get every flight from `fly_from` to `fly_to` in range of dates from `date_from` to `date_to`
    """
    url = 'https://api.skypicker.com/flights'
    params = {
        'fly_from': fly_from,
        'fly_to': fly_to,
        'date_from': date_from,
        'date_to': date_to,
        'partner': 'picky'
    }
    async with ClientSession() as session:
        async with session.get(url, params=params) as response:
            json = await response.json()
            return json['data']


async def check_flight(booking_token, bnum, pnum, currency, adults, children, infants):
    """
    Check if the flight is valid
    """
    url = 'https://booking-api.skypicker.com/api/v0.1/check_flights'
    params = {
        'booking_token': booking_token,
        'bnum': bnum,
        'pnum': pnum,
        'currency': currency,
        'adults': adults,
        'children': children,
        'infants': infants
    }
    async with ClientSession() as session:
        while True:
            async with session.get(url, params=params) as response:
                json = await response.json()
                if json['flights_checked']:
                    return json
