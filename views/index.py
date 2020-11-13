from aiohttp import web
from aiohttp_cache import cache
from datetime import date, datetime, time, timedelta
from flights import get_flights


DEFAULTS = {
    'date_from': date.today().strftime('%d/%m/%Y'),
    'date_to': (date.today() + timedelta(days=31)).strftime('%d/%m/%Y'),
}
EXPIRES = (datetime.combine(datetime.now() + timedelta(days=1), time.min) - datetime.now()).seconds


@cache(expires=EXPIRES)
async def index(request):
    flights = await get_flights(DEFAULTS['date_from'], DEFAULTS['date_to'])
    payload = []
    for flight in flights:
        payload.append({
            'fly_from': flight['flyFrom'],
            'fly_to': flight['flyTo'],
            'd_time_utc': datetime.fromtimestamp(flight['dTimeUTC']).strftime('%d/%m/%Y, %H:%M'),
            'a_time_utc': datetime.fromtimestamp(flight['aTimeUTC']).strftime('%d/%m/%Y, %H:%M'),
            'price': flight["price"]
        })
    return web.json_response(payload)
