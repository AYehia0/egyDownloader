import requests
from bs4 import BeautifulSoup as bs

#faster way to scrap better t
class Scrapper:
    
    def __init__(self, url):
        self.srcape_url = url
        self.qualities_sizies = []

        self.soup = self.init_soup()
        #self.list_all_info()

    def init_soup(self):
        self.r_url = requests.get(self.srcape_url).text
        self.soup = bs(self.r_url, 'lxml')

        return self.soup

    #gets type, quality and size of a movie
    def list_all_info(self):
        download_table = self.soup.find(class_='dls_table btns full mgb').tbody.find_all('tr')
        for i in range(5):
            for td in download_table[i].find_all('td'):
                x = td.find('a', class_="nop btn g dl _open_window")
                if td.text != " تحميل  مشاهدة ":
                    self.qualities_sizies.append(td.text)
                if x is not None:
                    self.qualities_sizies.append(x.get('data-url'))
                




