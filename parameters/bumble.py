from flask import Blueprint, render_template, request, redirect, url_for, flash
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
    InvalidSessionIdException,
    NoSuchWindowException
)
import time
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

add_mod = Blueprint('bumble', __name__, template_folder='templates')

class BumbleAutomation:
    """Class to handle Bumble automation using Selenium."""
    
    # Constants
    FACEBOOK_URL = 'https://www.facebook.com/'
    BUMBLE_URL = 'https://www.bumble.com/get-started'
    WAIT_TIMEOUT = 10
    
    def __init__(self, username: str, password: str):
        """Initialize the automation with credentials."""
        self.username = username
        self.password = password
        self.driver = self._setup_driver()
        
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and configure Chrome WebDriver."""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-popup-blocking')
            
            # Add your Chrome driver path here
            service = Service('path/to/your/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.implicitly_wait(self.WAIT_TIMEOUT)
            return driver
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise

    def _wait_for_element(self, by: By, value: str, timeout: int = WAIT_TIMEOUT) -> Optional[webdriver.remote.webelement.WebElement]:
        """Wait for an element to be present and return it."""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            logger.warning(f"Element not found: {value}")
            return None

    def _safe_click(self, element: webdriver.remote.webelement.WebElement) -> bool:
        """Safely click an element with error handling."""
        try:
            element.click()
            return True
        except WebDriverException as e:
            logger.error(f"Failed to click element: {str(e)}")
            return False

    def facebook_login(self) -> bool:
        """Handle Facebook login process."""
        try:
            self.driver.get(self.FACEBOOK_URL)
            
            # Login to Facebook
            email_field = self._wait_for_element(By.ID, "email")
            password_field = self._wait_for_element(By.ID, "pass")
            
            if not all([email_field, password_field]):
                raise NoSuchElementException("Facebook login fields not found")
                
            email_field.send_keys(self.username)
            password_field.send_keys(self.password)
            
            login_button = self._wait_for_element(By.NAME, "login")
            if not login_button or not self._safe_click(login_button):
                raise WebDriverException("Failed to click login button")
            
            # Verify successful login
            if not self._wait_for_element(By.ID, 'u_0_c'):
                flash("Invalid Facebook credentials")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Facebook login failed: {str(e)}")
            flash("Facebook login failed. Please try again.")
            return False

    def bumble_login(self, is_facebook: bool = True) -> bool:
        """Handle Bumble login process."""
        try:
            self.driver.get(self.BUMBLE_URL)
            
            if is_facebook:
                login_button = self._wait_for_element(By.XPATH, "//*[text()='Use Facebook']")
            else:
                login_button = self._wait_for_element(By.XPATH, "//*[text()='Use cell phone number']")
                
            if not login_button or not self._safe_click(login_button):
                raise WebDriverException("Failed to click Bumble login button")
            
            if not is_facebook:
                phone_field = self._wait_for_element(By.NAME, "phone")
                if not phone_field:
                    raise NoSuchElementException("Phone number field not found")
                phone_field.send_keys(self.username)
                
                continue_button = self._wait_for_element(By.XPATH, "//*[text()='Continue']")
                if not continue_button or not self._safe_click(continue_button):
                    raise WebDriverException("Failed to click continue button")
                
                password_field = self._wait_for_element(By.ID, "pass")
                if not password_field:
                    raise NoSuchElementException("Password field not found")
                password_field.send_keys(self.password)
                
                sign_in_button = self._wait_for_element(By.XPATH, "//*[text()='Sign In']")
                if not sign_in_button or not self._safe_click(sign_in_button):
                    raise WebDriverException("Failed to click sign in button")
            
            return self._verify_bumble_login()
            
        except Exception as e:
            logger.error(f"Bumble login failed: {str(e)}")
            flash("Bumble login failed. Please try again.")
            return False

    def _verify_bumble_login(self) -> bool:
        """Verify successful Bumble login."""
        try:
            self._wait_for_element(By.XPATH, "//*[@id=\"main\"]/div/div[1]/aside/div/div[2]/div")
            return True
        except NoSuchElementException:
            flash("Bumble login verification failed")
            return False

    def swipe_right(self) -> bool:
        """Perform swipe right automation."""
        swipe_count = 0
        max_swipes = 100  # Set a reasonable limit
        
        while swipe_count < max_swipes:
            try:
                # Try first swipe button
                button = self._wait_for_element(
                    By.XPATH,
                    "//*[@id=\"main\"]/div/div[1]/main/div[2]/div/div/span/div[2]/div/div[2]/div/div[3]/div/span/span"
                )
                
                if button and self._safe_click(button):
                    swipe_count += 1
                    time.sleep(2)
                    continue
                
                # Try alternative swipe button
                button = self._wait_for_element(
                    By.XPATH,
                    "//*[@id=\"main\"]/div/div[1]/main/div[2]/article/div/footer/div/div[2]/div/span/span/span"
                )
                
                if button and self._safe_click(button):
                    swipe_count += 1
                    time.sleep(2)
                    continue
                    
                # If no buttons found, check for out of likes
                flash("Daily swipe limit reached. Try again tomorrow.")
                return False
                
            except NoSuchWindowException:
                flash("Browser window was closed")
                return False
            except Exception as e:
                logger.error(f"Swipe right failed: {str(e)}")
                flash("An error occurred during swiping")
                return False
        
        flash(f"Completed {swipe_count} swipes")
        return True

    def cleanup(self):
        """Clean up resources."""
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logger.error(f"Cleanup failed: {str(e)}")

@add_mod.route('/bumble', methods=['GET', 'POST'])
def bumble():
    """Handle Bumble automation requests."""
    if request.method != 'POST':
        return redirect(url_for('home'))
        
    try:
        username = request.form.get("username") or request.form.get("cellphone")
        password = request.form.get("pwd")
        
        if not username or not password:
            flash("Please provide both username and password")
            return render_template("view.html")
            
        automation = BumbleAutomation(username, password)
        
        try:
            # Determine login method
            is_facebook = "username" in request.form
            
            if is_facebook:
                if not automation.facebook_login():
                    return render_template("view.html")
                    
            if automation.bumble_login(is_facebook):
                automation.swipe_right()
                
        finally:
            automation.cleanup()
            
        return render_template("view.html")
        
    except Exception as e:
        logger.error(f"Bumble automation failed: {str(e)}")
        flash("An unexpected error occurred")
        return render_template("view.html")
