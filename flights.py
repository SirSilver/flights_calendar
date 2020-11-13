from api import check_flight, fetch_flights
import asyncio
from datetime import date, timedelta
from helpers.parsers import parse_direction


DEFAULTS = {
    'bnum': 1,
    'pnum': 1,
    'currency': 'USD',
    'adults': 1,
    'children': 0,
    'infants': 0
}


def _get_filename(flight):
    return f'{flight["flyFrom"]}-{flight["flyTo"]}.json'


async def validate(flight):
    """
    Check if flight is valid or price has not been changed
    """
    check_response = await check_flight(
        flight['booking_token'],
        bnum=DEFAULTS['bnum'],
        pnum=DEFAULTS['pnum'],
        currency=DEFAULTS['currency'],
        adults=DEFAULTS['adults'],
        children=DEFAULTS['children'],
        infants=DEFAULTS['infants']
    )
    if check_response['flights_invalid']:
        return False
    if check_response['price_change']:
        if check_response['flights_price'] > flight['price']:
            return check_response['flights_price']
    return True


async def get_flight(fly_from, fly_to, date_from, date_to):
    """
    Find the flight with the lowest price from `fly_from` to `fly_to` in range
    of dates from `date_from` to `date_to`
    """
    flights = await fetch_flights(fly_from, fly_to, date_from, date_to)
    key = lambda flight: flight['price']

    while True:
        flight = min(flights, key=key)
        if valid_or_new_price := await validate(flight) is True:
            break
        elif valid_or_new_price is int:
            flight['price'] = valid_or_new_price
        else:
            flights.remove(flight)

    return flight


async def get_flights(date_from, date_to):
    """
    Get every cheapest flight between directions in `directions.txt`
    """
    tasks = []

    for n, direction in enumerate(open('directions.txt').readlines()):
        fly_from, fly_to = parse_direction(direction)
        tasks.append(get_flight(fly_from, fly_to, date_from, date_to))

    return await asyncio.gather(*tasks)
