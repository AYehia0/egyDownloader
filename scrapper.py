import requests
from bs4 import BeautifulSoup as bs

#faster way to scrap better t
class Scrapper:
    
    def __init__(self, url):
        self.srcape_url = url
        self.soup = self.init_soup()

    def init_soup(self):
        self.r_url = requests.get(self.srcape_url).text
        self.soup = bs(self.r_url, 'lxml')

        return self.soup

    #gets type, quality and size of a movie
    def get_movie_details(self):
        qualities_sizies = list()
        api_links = list()
        download_table = self.soup.find(class_='dls_table btns full mgb').tbody.find_all('tr')

        #5 is the number of all possible qualities, there is a better way to do it but i want to sleep now 
        try:
            for i in range(5):
                for td in download_table[i].find_all('td'):
                    x = td.find('a', class_="nop btn g dl _open_window")
                    if td.text != " تحميل  مشاهدة ":
                        qualities_sizies.append(td.text)
                    if x is not None:
                        api_links.append(x.get('data-url'))
        except Exception as e:
            print("Wrong page or still loading : " + e)
        return qualities_sizies, api_links               




