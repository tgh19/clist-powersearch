# Craigslist PowerSearch

Ever found a sweet deal on craigslist, but realized you were too late? 

This project was built to discover recent items posted on craigslist using multiple configurable queries to search for all of the items you want. Simply fill out queries in the `config.yml` and then run `python craig.py` (make sure to install `requirements.txt` too).

If you see a post you like, when prompted, enter `y` to save the post or press enter to blacklist the post. Blacklisting a post will add the post's URL to `blacklists.txt` so you don't have to look at it over and over again.

Current Features:
- Picture previews with link to original post
- Estimated distance based on your latitude and longitude
- Post blacklisting
- Results page with aggregation of all saved posts

Ideas For New Features:
- Better style on html
- Support for other browsers than chrome
- Support for macOS
- Front end
- Containerization
- And many more...
