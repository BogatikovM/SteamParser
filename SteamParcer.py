from bs4 import BeautifulSoup
import requests
import re

class SteamParser:
    def __init__(self, range = 100):
        self.url = "https://store.steampowered.com/search/?specials=1"
        self.range = range
        self.games = []
    def get_list(self):
        page = requests.get(self.url)
        status = page.status_code
        if status == 200:
            print("List created successfully:")
        else:
            print("Error")
        soup = BeautifulSoup(page.text, 'html.parser')
        unfiltered_games = soup.find_all(class_ = 'search_result_row', limit = self.range)
        for game in unfiltered_games:
            name = game.find(class_ = 'title')
            price = game.find(class_ = 'search_price_discount_combined').text.replace('\n', '.').replace('.', ' ').split()
            
            
            print(name.text, price)

ses = SteamParser(2)
ses.get_list()
