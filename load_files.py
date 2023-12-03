import json
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#loads url files into scraper from json
def load_data():
    file_path = 'url_list.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data
def fetch_price(title,price):
    my_list = [title[:28],price]
    
    with open('log_price.json','w') as file2:
        json.dump(my_list,file2)