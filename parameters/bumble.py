from flask import Blueprint, render_template,request,render_template,redirect, url_for, flash
from jinja2 import TemplateNotFound
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,InvalidSessionIdException,NoSuchWindowException
import time
import sys

add_mod =Blueprint('bumble',__name__,template_folder='templates')



class Check():
    def __init__(self,username,password):
        self.driver = webdriver.Chrome(<local chrome driver location>)
        self.username=username
        self.password=password


    def fb_login(self):
        self.driver.get('https://www.facebook.com/')
        self.driver.implicitly_wait(10)
        a = self.driver.find_element_by_id('email')
        a.send_keys(self.username)
        b = self.driver.find_element_by_id('pass')
        b.send_keys(self.password)
        c=self.driver.find_element_by_id('loginbutton')
        c.click()
        try:
            self.driver.find_element_by_id('u_0_c')
        except:
            flash("Invalid facebook username and password")
            self.driver.close()
            return False
        return True

    def facebook_login(self):
        self.driver.get("https://www.bumble.com/get-started")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//*[text()='Use Facebook']").click()
        return (self.check_sign_in())

    def cellphone_login(self):
        self.driver.get("https://www.bumble.com/get-started")
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//*[text()='Use cell phone number']").click()
        element = self.driver.find_element_by_id("phone")
        element.send_keys(self.username)
        self.driver.find_element_by_xpath("//*[text()='Continue']").click()
        try:
            element = self.driver.find_element_by_id("pass")
            element.send_keys(self.password)
            self.driver.find_element_by_xpath("//*[text()='Sign In']").click()
        except NoSuchElementException as e :
            self.driver.close()
            flash("Login failed: Verify username and password")
            return False
        return (self.check_sign_in())


    def check_sign_in(self):
        try:
            button = self.driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[1]/aside/div/div[2]/div")
        except NoSuchElementException:
            self.driver.close()
            flash("Login failed: Verify username and password")
            return False
        return True

    def swipe_right_fb(self):
        while True:
            try:
                button = self.driver.find_element_by_xpath(
                    "//*[@id=\"main\"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[3]/div/span/span")
                button.click()
            except:
                try:
                    button = self.driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[1]/main/div[2]/article/div/footer/div/div[2]/div/span/span/span")
                    button.click()
                except NoSuchElementException:
                    self.driver.quit()
                    flash("User out of likes: Wait until next day")
                    return(False)
                except NoSuchWindowException:
                    self.driver.quit()
                    flash("User closed google chrome window ")
                    return (False)
                except:
                    self.driver.quit()
                    flash("Check bumble issue")
                    return (False)


    def swipe_right_cellphone(self):
        while True:
            try:
                button = self.driver.find_element_by_xpath(
                    "//*[@id=\"main\"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[3]/div/span/span")
                button.click()
                time.sleep(2)
            except:
                try:
                    button = self.driver.find_element_by_xpath(
                        "//*[@id=\"main\"]/div/div[1]/main/div[2]/article/div/footer/div/div[2]/div/span/span/span")
                    button.click()
                except NoSuchElementException:
                    self.driver.quit()
                    flash(" User out of likes: Wait until next day")
                    return(False)
                except NoSuchWindowException:
                    self.driver.quit()
                    flash("User closed google chrome window ")
                    return (False)
                except:
                    self.driver.quit()
                    flash("Bumble got some issue")
                    return (False)




@add_mod.route('/bumble', methods=['GET', 'POST'])
def bumble():
    if "username" in request.form:
        sw = Check(request.form["username"],request.form["pwd"])
        if sw.fb_login():
            if (sw.facebook_login()):
                sw.swipe_right_fb()
                return render_template("view.html")
        else:
            return render_template("view.html")
    else:
        sw = Check(request.form["cellphone"], request.form["pwd"])
        if sw.cellphone_login():
            sw.swipe_right_cellphone()
            return render_template("view.html")
        else:
            return render_template("view.html")
