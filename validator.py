import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from GUI import *
class Formater():

    def findFormat(str):
        """
        find format file from way
        :param filename:
        :return:
        """
        #print(self)
        try:
            str = re.search(r"[a-zA-Z0-9\_\-\ ]+\.(csv|json|txt)", str).group(0)
        except:
            return None
        str = str.split(".")
        if len(str) == 2:
            return str[-1]

    def dataValidator(data,format):
        if format == "csv":
            pass
        if format == "json":
            pass
        if format == "txt":
            pass


class Validator():

    def __init__(self):
        #self.email = e
        #self.driver = d
        #self.is_alert = None
        self.error_email = []
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87")

        self.driver = webdriver.PhantomJS(executable_path='C:/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                                         desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
        #self.driver = webdriver.Firefox(executable_path='C:\\geckodriver_firefox\\\geckodriver.exe')


    def setEmail(self, e):
        self.email = e

    def get_result(self):
        """
        Email is Valid or isn`t valid
        :return:
        """
        if self.is_alert is True:
            return "The Email is valid"
        elif self.is_alert is False:
            return "The email is not valid"
        else:
            raise Exception("Error while executing")

    def get_error_email(self):
        """
        Items that do not match the email address
        :return:
        """
        if len(self.error_email) > 0:
            return self.error_email
        else:
            return None

    def grabber(self):
        if self.is_alert == True:
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            self.result = soup.find('div', id='ValidationResponse').find('div', class_='alert alert-success').get_text()
        if self.is_alert == False:
            page = self.driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            self.result = soup.find('div', id='ValidationResponse').find('div', class_='alert alert-danger').get_text()
            dangers = soup.find_all('li', class_='list-group-item')
            for item in dangers:
                if item.find('i', class_='icon-remove'):
                    error = item.get_text()
                    self.error_email.append(error[:-3])
        if self.is_alert == None:
            print("EROR GRABBER")

    def find_email_at_site(self):
        """
        search email at site http://www.emailvalidator.co
        :return:
        """
        #r = requests.get("http://www.emailvalidator.co")
        #if r.status_code != 200:
        #    raise r.status_code
        self.driver.get("http://www.emailvalidator.co")
        label_search = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "EmailAddress"))
        )
        #self.driver.set_window_size(1920, 1080)
        #self.driver.save_screenshot('test.png')
        label_search.clear()
        label_search.send_keys(self.email)
        buttom = WebDriverWait(self.driver, 5).until(
            #EC.presence_of_element_located((By.XPATH, 'button.yellow.large'))
            EC.presence_of_element_located((By.XPATH, "//div[@class='fl']//a[@class='button yellow large']"))
        )
        buttom.click()
        WebDriverWait(self.driver, 5)
        try:
            alert = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='span7']//div[@class='alert alert-success']"))
            )
            self.is_alert = True
        except:
            try:
                alert = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='span7']//div[@class='alert alert-danger']"))
                )
                self.is_alert = False
            except:
                self.is_alert = None
        finally:
            self.grabber()


    def close(self):
        """
        close webdriver
        :return:
        """
        self.driver.close()

"""
app = Validator()
app.setEmail("kanoru3101@gmail.com")
app.find_email_at_site()
print(app.get_result())
"""
"""
if __name__ == '__main__':

    app = Validator("kanoru3101@gmail.com")
    app.find_email_at_site()
    print(app.get_result())
    #driver.get("http://www.emailvalidator.co")
    #email_validator(driver)
    driver = webdriver.Firefox(executable_path='C:\\geckodriver_firefox\\\geckodriver.exe')
    app1 = Validator("kanoru3101@gmail.com")
    app1.find_email_at_site(driver)
    print(app1.get_result())
    print(app1.get_error_email())
    app2 = Validator("kanoru3101345@gmail.com")
    app2.find_email_at_site(driver)
    print(app2.get_result())
    print(app2.get_error_email())

"""
