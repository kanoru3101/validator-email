import requests
import re
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

    def __init__(self, e):
        self.email = e
        #self.driver = d
        #self.is_alert = None
        self.error_email = []

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
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            self.result = soup.find('div', id='ValidationResponse').find('div', class_='alert alert-success').get_text()
        if self.is_alert == False:
            page = driver.page_source
            soup = BeautifulSoup(page, 'lxml')
            self.result = soup.find('div', id='ValidationResponse').find('div', class_='alert alert-danger').get_text()
            dangers = soup.find_all('li', class_='list-group-item')
            for item in dangers:
                if item.find('i', class_='icon-remove'):
                    error = item.get_text()
                    print(error)
                    self.error_email.append(error[:-3])


    def find_email_at_site(self, drive):
        """
        search email at site http://www.emailvalidator.co
        :return:
        """
        r = requests.get("http://www.emailvalidator.co")
        if r.status_code != 200:
            raise r.status_code

        driver.get("http://www.emailvalidator.co")
        label_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "EmailAddress"))
        )
        label_search.clear()
        label_search.send_keys(self.email)
        buttom = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'button.yellow.large'))
        )
        buttom.click()
        WebDriverWait(driver, 5)
        is_alert = None
        try:
            alert = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'alert.alert-success'))
            )
            self.is_alert = True
        except:
            try:
                alert = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'alert.alert-danger'))
                )
                self.is_alert = False
            except:
                pass
        finally:
            self.grabber()

"""
if __name__ == '__main__':

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

