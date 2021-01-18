import requests
import json as js
from bs4 import BeautifulSoup as bs

# The autoCompletion link 
# https://egybest.site/autoComplete.php?q=saw

#faster way to scrap better t
class Scrapper:
    
    def __init__(self, url):

        self.scrape_url = url
        self.soup = self.init_soup()

    def init_soup(self):

        self.r_url = requests.get(self.scrape_url).text
        self.soup = bs(self.r_url, 'lxml')

        return self.soup

    #gets type, quality and size of a movie
    def get_movie_details(self):
        qualities_sizies = list()
        #5 is the number of all possible qualities, there is a better way to do it but i want to sleep now 
        try:
            download_table = self.soup.find(class_='dls_table btns full mgb')
            if download_table is not None:
                for tr in download_table.find_all('tr')[1:]:
                    tds = tr.find_all('td')
                    for td in tds[:3]:
                        qualities_sizies.append(td.text)
        except Exception as e:
            print("Wrong page or movie isn't available for download: " + e)
            return None
        return qualities_sizies              

    #searching using the autocomplete
    # {
    # "saw": [
    #     {
    #         "t": "Saw (2004)",
    #         "u": "movie/saw-2004",
    #         "i": "1984057894"
    #     },
    #     {
    #         "t": "Saw II (2005)",
    #         "u": "movie/saw-ii-2005",
    #         "i": "1984064979"
    #     },
    #     {
    #         "t": "Saw III (2006)",
    #         "u": "movie/saw-iii-2006",
    #         "i": "1984063562"
    #     },
    # ]
    # }
  

