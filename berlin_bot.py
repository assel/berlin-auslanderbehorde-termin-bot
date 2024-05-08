import time
import os
import logging
import playsound
from platform import system

import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

system = system()

default_time_sleep = 2
#max_time_resubmit = 60 * 15
max_time_resubmit = 60 * 7

sound_file = "alarm.wav"

logging.basicConfig(
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=logging.INFO,
)

class WebDriver:
    def __init__(self):
        self._driver: webdriver.Chrome

    def __enter__(self) -> webdriver.Chrome:
        logging.info("Open browser")
        # some stuff that prevents us from being locked out
        options = webdriver.ChromeOptions() 
        options.add_argument('--disable-blink-features=AutomationControlled')
        # debugging for windows: self._driver = webdriver.Chrome(os.path.join(os.getcwd(), "chromedriver"), options=options)
        self._driver = webdriver.Chrome(options=options)
        self._driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        return self._driver

    def __exit__(self, exc_type, exc_value, exc_tb):
        logging.info("Close browser")
        self._driver.quit()

class BerlinBot:
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self._sound_file = os.path.join(os.getcwd(), "alarm.wav")
        #de: self._error_message = """Für die gewählte Dienstleistung sind aktuell keine Termine frei! Bitte"""
        #en:
        self._error_message = """There are currently no dates available for the selected service! Please try again later."""
        ### english success_message still not known - this is only speculation right now
        #de: self._success_message = """Auswahl Uhrzeit"""
        #en: 
        self._success_message = """Select time"""
        self._timeout_message = """Sitzungsende"""
        self.start_time = time.time()

    def get_wait_time(self, init:list = [10, 20]):
        options = range(init[0], init[1], 1)
        chose_time = random.choice(options)
        return chose_time


    def clickPATH(self, path: str):
        time.sleep(default_time_sleep)
        try:
            WebDriverWait(self.driver, self.get_wait_time()).until(EC.element_to_be_clickable((By.XPATH, path)))
            self.driver.find_element(By.XPATH, path).click()
        except:
            self.clickPATH(path)

    
    def clickID(self, id: str):
        time.sleep(default_time_sleep)
        try:
            WebDriverWait(self.driver, self.get_wait_time()).until(EC.element_to_be_clickable((By.ID, id)))
            self.driver.find_element(By.ID, id).click()
        except:
            time.sleep(3)
            self.clickID(id)

    def select(self, id: str, text: str):
        time.sleep(default_time_sleep)
        try:
            element = self.driver.find_element(By.ID, id)   
            s = Select(element)
            s.select_by_visible_text(text)
        except:
            time.sleep(3)
            self.select(id, text)


    def enter_start_page(self):
        logging.info("Visit start page")
        #de: self.driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen")
        #en:
        self.driver.get("https://otv.verwalt-berlin.de/ams/TerminBuchen?lang=en")

        self.clickPATH('//*[@id="mainForm"]/div/div/div/div/div/div/div/div/div/div[1]/div[1]/div[2]/a')

    def tick_off_some_bullshit(self):
        logging.info("Ticking off agreement")

        self.clickPATH('//*[@id="xi-div-1"]/div[4]/label[2]/p')
        self.clickID('applicationForm:managedForm:proceed')
        time.sleep(5)

    def enter_form(self):
        
        # select Israel
        #de: self.wait_for_text("Staatsangehörigkeit")
        #en:
        self.wait_for_text("Citizenship")
        ###Israel
        self.select('xi-sel-400', 'Israel')
        ###Russia
        #self.select('xi-sel-400', 'Russian Federation')
    
        # one person
        #de: self.wait_for_text("Anzahl der Personen")
        #en:
        self.wait_for_text("Number of applicants")
        #de: self.select('xi-sel-422', 'eine Person')
        #en:
        self.select('xi-sel-422', 'one person')

        # no family
        #de: self.wait_for_text("Leben Sie in Berlin zusammen mit einem Familienangehörigen (z.B. Ehepartner, Kind)")
        #en:
        self.wait_for_text("Do you live in Berlin with a family member")
        #de: self.select('xi-sel-427', 'nein')
        #en:
        self.select('xi-sel-427', 'no')

        # first application
        self.clickPATH('//*[@id="xi-div-30"]/div[1]/label/p')

        # click employment -- ID depends on citizenship!
        ###Israel 
        self.clickPATH('//*[@id="inner-441-0-1"]/div/div[3]/label/p')
        ### Russia
        #self.clickPATH('//*[@id="inner-160-0-1"]/div/div[3]/label/p')

        # b/c of Erwerbstaetigkeit -- ID depends on citizenship and preselected language!!
        #de: self.clickPATH('//*[@id="SERVICEWAHL_DE441-0-1-1-328332"]')
        #en:
        ### Israel.Freelance (sect. 21 para. 5):
        self.clickPATH('//*[@id="SERVICEWAHL_EN441-0-1-1-328332"]')
        ### Israel.SelfEmployment (sect. 21):
        #self.clickPATH('//*[@id="SERVICEWAHL_EN441-0-1-1-305249"]')
        ### Israel.WorkVocationalTraining (sect. 18a):
        #self.clickPATH('//*[@id="SERVICEWAHL_EN441-0-1-1-305304"]')
        ### Israel.WorkAcademic (sect. 18b):
        #self.clickPATH('//*[@id="SERVICEWAHL_EN441-0-1-1-329328"]')
        
        ### Russia.Freelance (sect. 21 para. 5):
        #self.clickPATH('//*[@id="SERVICEWAHL_EN160-0-1-1-328332"]')
        ### Russia.SelfEmployment (sect. 21):
        #self.clickPATH('//*[@id="SERVICEWAHL_EN160-0-1-1-305249"]')
        ### Russia.WorkVocationalTraining (sect. 18a):
        #self.clickPATH('//*[@id="SERVICEWAHL_EN160-0-1-1-305304"]')
        ### Russia.WorkAcademic (sect. 18b):
        #self.clickPATH('//*[@id="SERVICEWAHL_EN160-0-1-1-329328"]')

        logging.info("Fill out form")


    def submit(self):
        wait_time = self.get_wait_time([default_time_sleep, default_time_sleep*2])
        time.sleep(wait_time)
        try:
            self.clickPATH('//*[@id="applicationForm:managedForm:proceed"]')
        except:
            logging.info("Retry fill out form")
            self.enter_form()
    
    def _success(self):
        logging.info("!!!SUCCESS - do not close the window!!!!")
        while True:
            self._play_sound(self._sound_file, 10)
            time.sleep(5)

    def wait_for_text(self, text: str, timeout: int = 60):
        while text not in self.driver.page_source:
            time.sleep(default_time_sleep)
            timeout -= 1
            if timeout == 0:
                raise TimeoutException("Timeout while waiting for text")
        time.sleep(default_time_sleep)

    @staticmethod
    def run_once():
        with WebDriver() as driver:
            bot = BerlinBot(driver)
            bot.enter_start_page()
            bot.tick_off_some_bullshit()
            bot.enter_form()
            time.sleep(default_time_sleep)
            driver.save_screenshot("screenshot_form.png")

            # retry submit
            while time.time() - bot.start_time < max_time_resubmit:
                bot.submit()
                logging.info("Current URL: " + driver.current_url)
                if bot._timeout_message in bot.driver.page_source or driver.current_url == "https://otv.verwalt-berlin.de/ams/TerminBuchen/logout":
                    ###Isopoda: debug print page source
                    with open("./page_source_session_timeout.html", "w", encoding='utf-8') as f:
                        f.write(driver.page_source)
                    logging.info("Session timeout - starting over")
                    bot.run_loop   
                elif bot._success_message in bot.driver.page_source \
                    or (not 'Family reasons' in driver.page_source and not bot._error_message in driver.page_source):
                    '''
                    # stolen at https://github.com/rasi-coder/berlin-auslanderbehorde-termin-bot
                    if not self._error_message in driver.page_source \
                            and not 'Familiäre Gründe' in driver.page_source \
                            and url_before != url_after:
                        current_window = driver.current_window_handle
                        driver.execute_script("alert(\"Focus window\")")
                        driver.switch_to.alert.accept()
                        driver.switch_to.window(current_window)
                        driver.fullscreen_window()
                        self._success()
                    '''
                    ###Isopoda: debug print page source
                    with open("./page_source_success.html", "w", encoding='utf-8') as f:
                        f.write(driver.page_source)
                    current_window = driver.current_window_handle
                    driver.execute_script("alert(\"Focus window\")")
                    driver.switch_to.alert.accept()
                    driver.switch_to.window(current_window)
                    driver.fullscreen_window()
                    bot._success()
                elif bot._error_message in bot.driver.page_source:
                    ###Isopoda: debug print page source
                    with open("./page_source_recent_error.html", "w", encoding='utf-8') as f:
                        f.write(driver.page_source)
                    logging.info("Retry submission - time passed: %.2f seconds." %(time.time() - bot.start_time))
                  
                else:
                    logging.info("max_time_resubmit reached")
                    pass

    @staticmethod
    def run_loop():
        # play sound to check if it works
        BerlinBot._play_sound(sound_file)
        while True:
            logging.info("One more round")
            BerlinBot.run_once()
            time.sleep(5)

    # stolen from https://github.com/JaDogg/pydoro/blob/develop/pydoro/pydoro_core/sound.py
    """@staticmethod
    def _play_sound(sound, t = 0):
        logging.info("Play sound")

        from playsound import playsound
        playsound(sound_file)
        time.sleep(t)"""

### ab hier Isopoda
    @staticmethod
    def _play_sound(sound, t=0):
            if system == "Darwin":
                #BerlinBot()._play_sound_osx(self._sound_file)
                BerlinBot(WebDriver())._play_sound_osx(sound_file) 
            elif system == "Windows":   
                #BerlinBot()._play_sound_windows(self._sound_file)             
                BerlinBot(WebDriver())._play_sound_windows(sound_file) 
            elif system == "Linux":
                BerlinBot(WebDriver())._play_sound_linux(sound_file)
            else:
                raise OSError("Sorry, I am not compatible with your OS (" + system +")")         

    # stolen from https://github.com/JaDogg/pydoro/blob/develop/pydoro/pydoro_core/sound.py
    @staticmethod
    def _play_sound_osx(sound, block=True):
        """
        Utilizes AppKit.NSSound. Tested and known to work with MP3 and WAVE on
        OS X 10.11 with Python 2.7. Probably works with anything QuickTime supports.
        Probably works on OS X 10.5 and newer. Probably works with all versions of
        Python.
        Inspired by (but not copied from) Aaron's Stack Overflow answer here:
        http://stackoverflow.com/a/34568298/901641
        I never would have tried using AppKit.NSSound without seeing his code.
        """
        from AppKit import NSSound
        from Foundation import NSURL
        from time import sleep

        logging.info("Play sound")
        if "://" not in sound:
            if not sound.startswith("/"):
                from os import getcwd

                sound = getcwd() + "/" + sound
            sound = "file://" + sound
        url = NSURL.URLWithString_(sound)
        nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
        if not nssound:
            raise IOError("Unable to load sound named: " + sound)
        nssound.play()

        if block:
            sleep(nssound.duration())

    @staticmethod
    def _play_sound_windows(sound, block=True):
        import winsound
        logging.info("Play sound")
        winsound.PlaySound(sound, winsound.SND_FILENAME)

    @staticmethod
    def _play_sound_linux(sound, block=True):
        from playsound import playsound
        logging.info("Play sound")
        playsound(sound)        

if __name__ == "__main__":
    BerlinBot.run_loop()
