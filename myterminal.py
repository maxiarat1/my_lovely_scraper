import os
import time
from colorfull_terminal import style, borders

def check_diff(new_item, existing_items):
    for item in existing_items:
        if item.title == new_item.title:
            return False
    return True

def fetch_data(item):
    return {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'tag': item.title,
        'price': item.price
    }
    
def print_dashboard(items_data):
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    print(f"======= DASHBOARD ({items_data[0]['timestamp'] }) =======")
    print(borders.border)
    for item_data in items_data:
        print(f"{style.YELLOW+item_data['tag'][:28]}{style.RESET}")
        print(f"{style.GREEN+item_data['price']}{style.RESET}")
        print(borders.border)
    print("=========================")
    print(u'[\N{EURO SIGN}]')

def start_terminal(items):
    try:
        items_data = [fetch_data(item) for item in items]
        print_dashboard(items_data)
        time.sleep(5)  # Update every 5 seconds
    except KeyboardInterrupt:
        print("Program interrupted by user, shutting down.")
        exit()

# Example usage
#items = [Item("Item 1", "$10"), Item("Item 2", "$20")]
#start_terminal(items)
