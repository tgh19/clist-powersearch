"""Find stuff you're interested in on Craigslist"""

# Standard lib
import os
import webbrowser
from datetime import datetime
from io import BytesIO

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

# Cleanup old results
if os.path.exists('results.html'):
    os.remove('results.html')

# Create page header
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
with open('results.html', 'w') as results_page:
    results_page.write(f"""
        <h1>Craigslist PowerSearch Results</h1>
        </br>
        Time: {current_time}
        </br>
    """)

# Make images folder if it dne
if not os.path.exists('images'):
    os.makedirs('images')

# Cleanup old images
for file_name in os.listdir('./images/'):
    if file_name.endswith('.png'):
        print(f'removing {file_name}')
        os.remove(os.path.join('./images/', file_name))


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


def create_html_page(post):
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
    for query in QUERIES:
        category = query[1]
        query = query[0]

        print(f'\nquerying {query} in category {category}')

        # Custom category
        if category == 'gym':
            category = 'sss?excats=7-13-22-2-24-1-23-2-1-1-2-9-10\
                -1-1-1-2-2-8-1-1-1-1-1-4-1-3-1-3-1-1-1-1-7-1-1-\
                1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-2-1-1-1-2-1-1\
                -1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-1-2-1'

        for_sale = CraigslistForSale(
            site='austin',
            category=category,
            filters={
                'query': query,
                'has_image': True,
                'posted_today': True
            }
        )

        results = for_sale.get_results(
            sort_by='newest',
            geotagged=True,
            include_details=True
        )

        i = 0
        for result in results:
            if i >= 3:
                break

            i += 1

            url = result.get('url')
            name = result.get('name').upper()
            details = result.get('body')
            distance = geodesic(MY_LAT_LONG, result.get('geotag')).miles

            blacklist = load_blacklist()
            if url in blacklist:
                print(f'post blacklisted: {name}')
                continue

            image_name = f'images/{query}_{i}.png'

            post = f"""
            <hr class="solid">
            <h2>{name}</h2>
            <p>
            <a href="{url}">
            <img src="{image_name}" height=200>
            </a>
            </br></br>
            Price: {result.get('price')}
            </br>
            Distance: {round(distance, 2)} miles
            </br>
            Details: {details}
            </br>
            </p>
            """

            response = requests.get(result.get('images')[0])
            img = Image.open(BytesIO(response.content))
            img.save(fp=image_name, format='png')
            create_html_preview(post=post)

            save = input('save? (y): ')

            if save == 'y':
                create_html_page(post=post)
            else:
                os.remove(image_name)
                with open('blacklist.txt', 'a') as bl_file:
                    bl_file.write(f'{url}\n')

    open_html('results.html')


if __name__ == '__main__':
    main()
