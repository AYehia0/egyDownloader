import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapper import Scrapper

class Egydownloader:

    def __init__(self, url):
        #download_url is the given link from the user
        self.download_url = url
        self.init_url = "https://beta.egybest.direct"
        self.driver_path = '/home/none/Desktop/github/egy-downloader/geckodriver'
        self.max_wait_time = 10
        self.driver = webdriver.Firefox(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.driver, self.max_wait_time)
        self.sc = Scrapper(self.download_url)
        self.sc.list_all_info()
        

    def get_link(self):
        #getting the egybest page
        self.driver.get(self.download_url)


    def bypass_egybest_popup(self):
        #clicking on the main board opens popup

        #check if 
        self.driver.find_element_by_id('main').click()
        


    def terminate_popup(self):
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)

            #closing all tabs expect the one which has the url
            if self.driver.current_url != self.download_url:
                time.sleep(3)
                self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])

        #  for i in reversed(range(1, len(self.chrome_driver.window_handles))):
        #     self.chrome_driver.switch_to.window(self.chrome_driver.window_handles[i])
        #     self.chrome_driver.close()
        
    
    def display_info(self):
        self.sc.list_all_info()
        info = self.sc.qualities_sizies

        #printing qualities
        for i in range(0, len(info), 3):
            print(*info[i:i+3], sep=' | ')

    def get_heighest(self):
        #self.driver.get(self.init_url + self.sc.qualities_sizies[3])
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="watch_dl"]/table/tbody/tr[1]/td[4]/a[1]' ))).click()
            


down = Egydownloader('https://beta.egybest.direct/movie/tenet-2020/')
down.get_link()
down.bypass_egybest_popup()
down.terminate_popup()
down.get_heighest()
#down.get_heighest()

