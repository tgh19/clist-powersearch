# pylint: disable= import-error, bare-except

"""Find stuff you're interested in on Craigslist"""

# Standard lib
import time

# Third party
from craigslist import CraigslistForSale
from geopy.distance import geodesic

# Local
from email_me import send_email
from helpers import get_default, load_blacklist, get_queries
from helpers import blacklist_result

# Globals
LAT_LONG = (get_default('latitude'), get_default('longitude'))
SLEEP_TIME = get_default('sleep_time')
MODE = get_default('mode')


def email_results(results, max_results):
    """Email the results from a query"""
    i = 0
    for result in results:
        if i >= max_results:
            break

        i += 1
        url = result.get('url')
        price = result.get('price')
        name = result.get('name').upper()
        distance = result.get('geotag')
        distance = round(geodesic(LAT_LONG, distance).miles, 2)
        blacklist = load_blacklist() # Reload blacklist each time

        if url in blacklist:
            print(f'skipping blacklisted post: {name}')
            continue

        send_email(f'{name} - {distance} mi - {price} - {url}')
        blacklist_result(url)


def main():
    """Run the main procedure"""
    for query in get_queries():
        search = query.get('query')
        city = query.get('city', get_default('city'))
        sort_by = query.get('sort_by', get_default('sort_by'))
        category = query.get('cat', None)
        max_results = query.get('max', get_default('max_results'))
        posted_today = query.get('posted_today', get_default('posted_today'))

        print('\nRUNNING QUERY:'.upper())
        print(f' - city: {city}')
        print(f' - query: {search}')
        print(f' - sort_by: {sort_by}')
        print(f' - category: {category}')
        print(f' - max_results: {max_results}')
        print(f' - posted_today: {posted_today}')

        # Custom category for gym
        if category == 'gym':
            category = 'sss?excats=7-13-22-2-24-1-23-2-1-1-2-9-10\
                -1-1-1-2-2-8-1-1-1-1-1-4-1-3-1-3-1-1-1-1-7-1-1-\
                1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-2-1-1-1-2-1-1\
                -1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-1'

        for_sale = CraigslistForSale(
            site=city,
            category=category,
            filters={
                'query': search,
                'has_image': True,
                'posted_today': posted_today
            }
        )

        results = for_sale.get_results(
            sort_by=sort_by,
            geotagged=True,
            include_details=True
        )

        if MODE == 'email':
            email_results(results, max_results)
        else:
            print(f'mode {MODE} not supported')


if __name__ == '__main__':
    while True:
        try:
            main()
            send_email('successfully ran queries')
        except:
            send_email('something went wrong')

        print(f'sleeping {SLEEP_TIME} min...')
        time.sleep(int(SLEEP_TIME)*60)
