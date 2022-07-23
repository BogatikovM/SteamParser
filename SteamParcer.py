from bs4 import BeautifulSoup
import requests


class SteamParser:
    def __init__(self):
        self.url = "https://store.steampowered.com/search/?specials=1"
        self.length = 50
        self.games = {}
    def set_length(self, length):
        try:
            self.length = int(length)
        except ValueError:
            print('Incorrect length value (default value: 50)')
    def get_list(self):
        page = requests.get(self.url)
        status = page.status_code
        if status == 200:
            print("List created successfully")
        else:
            print("Error")
        soup = BeautifulSoup(page.text, 'html.parser')
        raw_games = soup.find_all(class_ = 'search_result_row', limit = self.length)
        for game in raw_games:
            name = game.find(class_ = 'title').text
            price = game.find(class_ = 'search_price_discount_combined').text.replace('\n', '.').replace('.', ' ').split()
            price[1], price[3] = float(price[1].replace(',', '.')), float(price[3].replace(',', '.'))
            self.games[name] = price
    def sort_list(self, order:str):
        if order == 'h_to_l':
            rev = True
        else:
            rev = False
        self.games = dict(sorted(self.games.items(), key=lambda item: item[1][3], reverse=rev))
    def print_to_terminal(self):
        for k, v in self.games.items():
            print(k,' ||| ', *v)
    def print_to_file(self, file:str):
        try:
            with open(file, 'w') as f:
                for k, v in self.games.items():
                    f.write(f'{k} ||| {" ".join(str(x) for x in v)} \n')
        except FileNotFoundError:
            print('File name error! (default name: steam_list.txt)')
            self.print_to_file('steam_list.txt')



if __name__ == '__main__':
    length = input('Insert length of a list: ')
    order = input('Insert order of sorting (h_to_l / l_to_h): ')
    output = input('Way of output (terminal / file): ')
    if output == 'file':
        file = input('Insert file name: ')

    lst = SteamParser()
    lst.set_length(length)
    lst.get_list()
    lst.sort_list(order)
    if output == 'file':
        lst.print_to_file(file)
    else:
        lst.print_to_terminal()
