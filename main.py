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
        self.driver_path = 'driver/geckodriver'
        self.max_wait_time = 10

        self.driver = webdriver.Firefox(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.driver, self.max_wait_time)
  
    def get_table_info(self):
        self.sc = Scrapper(self.download_url)
        return self.sc.qualities_sizies

    def get_link(self):
        try:
            #tring to open the page
            self.driver.get(self.download_url)
        except Exception as e:
            print(e)

    def click_somewhere(self):
        self.driver.find_element_by_id('main').click()
        
    #index_to_terminate 0: for first, 1 for second
    def terminate_popup(self, index_to_terminate=0):

        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)

            #closing all tabs expect the one which has the url
            if self.driver.current_url != self.download_url:
                time.sleep(3)
                self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[index_to_terminate])
        
    #prints the contents of the table
    def display_info(self):
        info = self.get_table_info()
        #printing qualities
        for i in range(0, len(info), 3):
            print(*info[i:i+3], sep=' | ')

    def get_download_quality(self, index):
        #self.driver.get(self.init_url + self.sc.qualities_sizies[3])
        time.sleep(3)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="watch_dl"]/table/tbody/tr[{index}]/td[4]/a[1]' ))).click()
            

    def check_for_popups(self):
        #it clicks somewhere, where it doesn't redirect
        #if another tab is opened -> there is a popup, close it else after 2 seconds continue
        self.get_link()

        try:
            self.click_somewhere()
            time.sleep(5)
            if len(self.driver.window_handles) > 1:
                #there is a popup
                print(f"a pop up is there : {len(self.driver.window_handles)} opened tabs")
                self.terminate_popup(0)
                time.sleep(3)

        except :
            print("nothing")
            self.get_download_quality(1)
            #close the movie page
            self.terminate_popup(0)


    def work(self):
        #self.display_info()

        #checking for popups
        self.check_for_popups()

        self.get_download_quality(1)



down = Egydownloader('https://beta.egybest.direct/movie/tenet-2020/')

down.work()

