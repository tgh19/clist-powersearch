"""Find stuff you're interested in on Craigslist"""

# Standard lib
import os
import webbrowser
from datetime import datetime
from io import BytesIO
import shutil

# Third party
import requests
from craigslist import CraigslistForSale
from geopy.distance import geodesic
from PIL import Image
import yaml


with open('config.yml') as config_file:
    CONFIG = yaml.load(config_file, yaml.Loader)

def get_default(param, config=CONFIG):
    return config.get('default params').get(param)

# Load lat long from config
lat = get_default('latitude')
lng = get_default('longitude')
MY_LAT_LONG = (lat, lng)

# Cleanup old results page
if os.path.exists('results.html'):
    os.remove('results.html')

# Create page header
now = datetime.now()
current_time = now.strftime("%A %I:%M %p")
with open('results.html', 'w') as results_page:
    results_page.write(
        f"""
            <!DOCTYPE html>
            <html>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://www.w3schools.com/w3css/3/w3.css">
            <head>
                <title>
                    Craigslist PowerSearch Results
                </title>
            </head>
            <body>
                <h1 style="text-align:center">
                    Craigslist PowerSearch Results
                </h1>
                <p style="text-align:center">
                    {current_time}
                </p>
            </br>
        """
    )

# Make images folder if it dne
if not os.path.exists('images'):
    os.makedirs('images')

# Cleanup old images
for file_name in os.listdir('./images/'):
    if file_name.endswith('.png'):
        print(f'removing {file_name}')
        os.remove(os.path.join('./images/', file_name))

# Create blacklist file if it doesn't exist
if not os.path.exists('blacklist.txt'):
    open('blacklist.txt', 'w+')


def open_html(url):
    """open url in chrome"""
    webbrowser.register(
        name='chrome',
        klass=None,
        instance=webbrowser.BackgroundBrowser(
            "C://Program Files (x86)//Google//Chrome//Application//chrome.exe"
        )
    )
    webbrowser.get('chrome').open(url)


def create_html_preview(post):
    """creates an html page to preview post"""
    if os.path.exists('preview.html'):
        os.remove('preview.html')

    with open('preview.html', 'w') as preview:
        preview.write('\n')
        try:
            preview.write(post)
        except UnicodeEncodeError:
            preview.write(str(post.encode('utf-8')))

    open_html('preview.html')


def add_post_to_result_page(post):
    """creates an html result page"""
    print('Writing page')
    with open('results.html', 'a+') as page:
        page.write('\n')
        try:
            page.write(post)
        except UnicodeEncodeError:
            page.write(str(post.encode('utf-8')))


def load_blacklist():
    """Load in blacklisted posts"""
    with open('blacklist.txt') as bl_file:
        blacklist = []
        for url in bl_file:
            blacklist.append(url[:-1])
        return blacklist


def main():
    """Run the main procedure"""
    for query_params in CONFIG.get('queries'):
        query = query_params.get('query')
        city = query_params.get('city', get_default('city'))
        sort_by = query_params.get('sort_by', get_default('sort_by'))
        category = query_params.get('cat', None)
        max_results = query_params.get('max', get_default('max_results'))
        posted_today = query_params.get('posted_today', get_default('posted_today'))

        print('\nRUNNING QUERY:'.upper())
        print(f' - city: {city}')
        print(f' - query: {query}')
        print(f' - sort_by: {sort_by}')
        print(f' - category: {category}')
        print(f' - max_results: {max_results}')
        print(f' - posted_today: {posted_today}\n')

        print('RESULTS')

        # Custom category
        if category == 'gym':
            category = 'sss?excats=7-13-22-2-24-1-23-2-1-1-2-9-10\
                -1-1-1-2-2-8-1-1-1-1-1-4-1-3-1-3-1-1-1-1-7-1-1-\
                1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-2-1-1-1-2-1-1\
                -1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-1'

        for_sale = CraigslistForSale(
            site=city,
            category=category,
            filters={
                'query': query,
                'has_image': True,
                'posted_today': posted_today
            }
        )

        results = for_sale.get_results(
            sort_by=sort_by,
            geotagged=True,
            include_details=True
        )

        i = 0
        for result in results:
            if i >= max_results:
                break

            i += 1

            post_id = result.get('id')
            url = result.get('url')
            name = result.get('name').upper()
            details = result.get('body')
            distance = round(geodesic(MY_LAT_LONG, result.get('geotag')).miles, 2)

            # Reload blacklist each time 
            blacklist = load_blacklist()

            if url in blacklist:
                # Don't count blacklisted post as a result
                i -= 1 
                print(f'skipping blacklisted post: {name}')
                continue

            image_filenames = [f'images/{post_id}_{j}.png' for j, item in enumerate(result.get('images'))]

            image_html = ''
            for filename in image_filenames:
                image_html += f'<img src="{filename}" height=200> '

            # Build post HTML dynamically
            post = f"""
                <!DOCTYPE html>
                <html>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://www.w3schools.com/w3css/3/w3.css">
                <hr class="solid">

                <h4 style="text-align:center">
                    {name}
                </h4>
                
                <p style="padding: 35px">
                    <a href="{url}">
                        {image_html}
                    </a>
                    </br></br>
                        <b>Price:</b> {result.get('price')}
                    </br>
                        <b>Distance:</b> {distance} miles
                    </br>
                        <b>Details:</b> {details}
                    </br>
                </p>
            """
            for i, image_filename in enumerate(image_filenames):
                image_data = requests.get(result.get('images')[i])
                image_file = Image.open(BytesIO(image_data.content))
                image_file.save(fp=image_filename, format='png')

            create_html_preview(post=post)

            save = input('save this post? (y,n): ')

            if save == 'y':
                add_post_to_result_page(post=post)
            else:
                for image_filename in image_filenames:
                    os.remove(image_filename)
                with open('blacklist.txt', 'a+') as bl_file:
                    bl_file.write(f'{url}\n')

    open_html('results.html')


if __name__ == '__main__':
    main()
