# Craigslist PowerSearch

Ever found a sweet deal on craigslist, but realized you were too late? 

This project was built to discover recent items posted on craigslist using multiple configurable queries to search for all of the items you want. Simply fill out queries in the `config.yml` (use `config.example.yml` as a guide), ensure docker and docker-compose are installed, then run `docker-compose up -d`.

You can create a new gmail account and enter its credentials for the source email in `email_me.py`, then set the recipient address to be your cell provider's email to sms address. For instance {phone_number}@vtext.com for verizon.

