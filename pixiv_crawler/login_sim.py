# import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# import time

def login_for_cookies(config):
    login_url='https://accounts.pixiv.net/login'
    pixiv_root="https://www.pixiv.net/"
    
    service_args=[]
    if config.proxies_enable:
        service_args.extend([ '--proxy={0}'.format(config.socks), '--proxy-type=socks5', ])

    if config.phantomjs:
        driver = webdriver.PhantomJS(executable_path = config.phantomjs,service_args=service_args)
    if config.firefox:
        options=webdriver.firefox.options.Options()
        options.add_argument('-headless')
        driver = webdriver.Firefox(executable_path = config.firefox,service_args=service_args, firefox_options=options)
    if config.chrome:
        options=webdriver.chrome.options.Options()
        options.add_argument('-headless')
        driver = webdriver.Chrome(executable_path = config.chrome,service_args=service_args, chrome_options=options)
        

    driver.get(login_url)
    login_e=driver.find_element_by_xpath("//div[@id='container-login']")
    # print(login_e)
    username_e=login_e.find_element_by_xpath(".//input[@type='text']")
    # print(username_e)
    username_e.send_keys(config.username)
    password_e=login_e.find_element_by_xpath(".//input[@type='password']")
    # print(password_e)
    password_e.send_keys(config.password)
    login_button=login_e.find_element_by_xpath(".//button")
    login_button.click()
    
    # print(driver.page_source)
    
    try:
        # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']/div[@class='recaptcha-checkbox-checkmark']"))).click()
        element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.ID, "root"))
            )
    except Exception as e:
        driver.save_screenshot("./temp/log_in_err.png")
        driver.quit()
        raise IOError("login sim wait failed, 'root' did not appear")
    
    cookies_dict=dict()
    cookies=driver.get_cookies()
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']

    driver.quit()
        
    return cookies_dict
    
if __name__=="__main__":
    class Config(object):
        def __init__(self):
            self.username=""
            self.password=""
            self.proxies_enable = True
            self.socks = ""
            # self.phantomjs = "D:/tectree/Code/phantomjs-2.1.1-windows/bin/phantomjs.exe"
            self.phantomjs = "/Users/yuehan/tectree/Code/phantomjs-2.1.1-macosx/bin/phantomjs"
            self.firefox=""
            self.chrome=""
            
    config=Config()
    
    cookies=login_for_cookies(config)
    print(cookies)
