import os
import threading
import time
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from myterminal import start_terminal
from load_files import load_data,fetch_price
from colorfull_terminal import style

class Item:
    """ Represents an item with title, price, and date. """

    def __init__(self, title='', price='', date=''):
        self.title = title
        self.price = price
        self.date = date

def website_scraped(url_List, targ_List, pitem):
    """ Scrapes a website for product information.

    Args:
        url_List (dict): A dictionary containing URL and ID.
        pitem (list): A list to store scraped items.
    """
    try:
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Brave/701.0.3626.121 Safari/537.36'),
            'Accept-Language': 'en-US,en;q=0.2'
        }
        response = requests.get(url_List["url"], headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            pt = soup.find(targ_List['t_tag'],attrs={targ_List['t_key']:targ_List['t_var']})
            pp = soup.find(targ_List['p_tag'],attrs={targ_List['p_key']:targ_List['p_var']})
            if pt and pp:
                title = pt.get_text().strip()
                price = pp.get_text().strip()
                with lock:
                    pitem.append(Item(title, price))    
                fetch_price(title,price)
        else:
            print(f'{style.RED}Error while connecting{style.RESET}')
    except requests.exceptions.ConnectionError:
        print(f'{style.RED}Failed to resolve:{style.RESET}', url_List["url"])
    except AttributeError:
        print(f"{style.RED}'NoneType' object has no attribute 'string'{style.RESET}")

def run_scraper(data):
    """ Runs the scraper on multiple threads. """
    pitem = []
    threads = []
    for url in data['urls']:
        for targ in data['targ']:
            if url['id']==targ['id']:
                thread = threading.Thread(target=website_scraped, args=(url, targ, pitem))
                threads.append(thread)
                thread.start()

    for thread in threads:
        thread.join()
    start_terminal(pitem)

# Setting the current directory to the script location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Scheduler settings
delay = 60
lock = threading.Lock()
scheduler = BackgroundScheduler()
data = load_data()

# Scheduling and running the scraper
run_scraper(data)
scheduler.add_job(run_scraper, 'interval',args=[data], seconds=delay, max_instances=1)
scheduler.start()

try:
    # Keep the main thread alive
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program interrupted by user, shutting down.")
    scheduler.shutdown()
