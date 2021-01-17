import time
import requests
import json as js
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapper import Scrapper

class Egydownloader:

    def __init__(self, user_input):
        #download_url is the given link from the user
        self.download_url = user_input
        
        #self.init_url = "https://beta.egybest.direct/"
        self.driver_path = 'driver/geckodriver'
        self.vid_options = None
        self.vid_api_calls = None
        self.quality_index = None
        self.max_wait_time = 10
        self.base_url = "https://nero.egybest.site/"
        self.auto_complete = "autoComplete.php?q="
        self.driver = None
        self.wait = None
        
        if "https" not in self.download_url:
            self.search_key = self.download_url
            self.get_full_url()


    #in case of the download url is actually the search key
    def search_movie(self):
        search_out_names = []
        search_out_ids = []

        try:
            res_txt = js.loads(requests.get(self.base_url  + self.auto_complete + self.search_key).text)

            for i in res_txt[self.search_key]:
                
                #Saw V (2008)
                search_out_names.append(i['t'])
                
                #movie/saw-v-2008
                search_out_ids.append(i['u'])

        except Exception as e:
            print(e)
        
        return search_out_names, search_out_ids

    #get the full url in case of searching 
    def get_full_url(self):

        movie_names, movie_ids = self.search_movie()
        #print all the movies
        print("All available movies...")
        print("----------------")
        for index, movie in enumerate(movie_names, start=1 ):
            print(f"{index} : {movie}")
        
        print("----------------")
        while True:
            movie_choice = int(input("Choose a movie..."))
            if movie_choice in range(1, len(movie_names)+1):
                self.download_url = self.base_url + movie_ids[movie_choice-1]
                #print(self.download_url)
                return
            else:
                print("Invalid choice")

    def init_webdriver(self):
        self.driver = webdriver.Firefox(executable_path=self.driver_path)
        self.wait = WebDriverWait(self.driver, self.max_wait_time)
  

    def get_table_info(self):
        try:
            self.sc = Scrapper(self.download_url)
            details_movie = self.sc.get_movie_details()

        except Exception as e:
            print("Error initializing the Scrapper: " + e)
        return details_movie


    def get_download_button(self, url):
        self.sc = Scrapper(url)
        self.sc.vidstram_link()

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

        for _ in self.driver.window_handles:
            #self.driver.switch_to.window(handle)

            #closing all tabs expect the one which has the url
            if self.driver.current_url != self.download_url:
                time.sleep(3)
                self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[index_to_terminate])
        
    def close_home(self, index=0):
        #print(len(self.driver.window_handles))
        for i in reversed(range(1, len(self.driver.window_handles))):
            self.driver.switch_to.window(self.driver.window_handles[i])
            #print(self.driver.current_url)
            if "vidstream" not in self.driver.current_url:
                self.driver.close() 
        self.driver.switch_to.window(self.driver.window_handles[index])

    #prints the contents of the table
    def display_info(self):
        self.vid_options = self.get_table_info()
        
        #printing qualities
        for i in range(0, len(self.vid_options), 3):
            print(*self.vid_options[i:i+3], sep=' | ')

    def get_quality_choice(self):
        choices = int(len(self.vid_options) / 3)
        while True:
            q = int(input("Please choose a quality to download: "))

            if q in range(1, choices+1):
                print("Please wait while fetching the link...")
                print("----------------")
                self.quality_index = q 

                return
            else:
                print("Invalid option")


    def get_download_quality(self):
        #self.driver.get(self.init_url + self.sc.qualities_sizies[3])
        #time.sleep(3)
        index = self.quality_index
        try:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="watch_dl"]/table/tbody/tr[{index}]/td[4]/a[1]' ))).click()
        except Exception as e:
            print("Time out: " + e)       

    def check_for_popups(self):
        #it clicks somewhere, where it doesn't redirect
        #if another tab is opened -> there is a popup, close it else after 2 seconds continue
        self.get_link()

        try:
            self.click_somewhere()
            time.sleep(2)
            if len(self.driver.window_handles) > 1:
                #there is a popup
                #print(f"a pop up is there : {len(self.driver.window_handles)} opened tabs")
                self.close_home()
                time.sleep(2)

        except :
            print("nothing")
            self.get_download_quality()
            
    def get_page_tabs(self, name):
        try:
            for i in reversed(range(1, len(self.driver.window_handles))):
                self.driver.switch_to.window(self.driver.window_handles[i])
                #print(self.driver.current_url)
                if name in self.driver.current_url:
                    self.driver.switch_to.window(self.driver.window_handles[i])
        except Exception as e:
            print("failed " + e)

    def vidstream(self):
        try:
            target = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/p/a[1]'))).get_attribute('href')
        except Exception as e:
            print(e)
        return target

    def driver_quit(self):
        try:
            self.driver.quit()
        except :
            print("already closed")


    def work(self):
        


        self.display_info()

        print("----------------")
        self.get_quality_choice()


        # starting the webdriver after scraping
        self.init_webdriver()

        #checking for popups
        self.check_for_popups()

        self.get_download_quality()
        time.sleep(2)
        
        #switch to the vidstream page
        self.get_page_tabs('vidstream')

        time.sleep(3)
        self.driver.find_element_by_class_name('bigbutton').click()
        self.get_page_tabs('vidstream')

        time.sleep(5)
        #the link ,woah
        print("The Download Link : " + self.vidstream())
        
        # quitting 
        self.driver_quit()

    

# https://beta.egybest.direct/movie/we-can-be-heroes-2020/?ref=movies-p2    
user_input = input("Movie: ")
print("----------------")
down = Egydownloader(user_input)


down.work()

