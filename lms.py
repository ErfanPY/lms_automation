import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


uni_classes = {
    "computer_architecture": {
        "id": "5358",
        "name": "class-26-195045-2616414-2"
    },
    "physic_2": {
        "id": "5610",
        "name": "class-26-196596-2606008-2"
    }
}


def join_a_class(username, password, class_id, class_name):
    driver = webdriver.Chrome('chromedriver')
    driver.get("https://lms.birjand.ac.ir/login/index.php")

    WebDriverWait(driver, 200).until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, "input#username")))

    fill_input(driver, "username", username)
    fill_input(driver, "password", password)

    # check_recaptcha(driver)

    driver.find_element_by_id("loginbtn").click()

    session_id = get_session_id(driver, class_id)

    adobe_url = f"https://ac1.birjand.ac.ir/{class_name}/?session={session_id}&proto=true"
    driver.get(adobe_url)

    open_in_browser_button = driver.find_element_by_css_selector(
        ".addin-not-forced .button-style")
    open_in_browser_button.click()


def fill_input(driver, name, value):
    elem = driver.find_element_by_name(name)
    elem.send_keys(value)


def check_recaptcha(driver):
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(
        (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))

    recaptcha_XPATH = "//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox']/div[@class='recaptcha-checkbox-checkmark']"
    driver.execute_script("arguments[0].click();", WebDriverWait(
        driver, 10).until(EC.element_to_be_clickable((By.XPATH, recaptcha_XPATH))))
    checked_recaptcha_XPATH = "//span[@class='recaptcha-checkbox goog-inline-block recaptcha-checkbox-unchecked rc-anchor-checkbox recaptcha-checkbox-checked']"

    try:
        WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, checked_recaptcha_XPATH)))
    except:
        print("Couldn't solve reCaptcha.")

    driver.switch_to.default_content()


def get_session_id(driver, class_id, ):
    headers = {'cookie': 'MoodleSession=' +
               driver.get_cookie("MoodleSession")['value']}
    params = (('id', class_id), ('action', 'join'))
    response = requests.post(
        'https://lms.birjand.ac.ir/mod/onlineclass/view.php', headers=headers, params=params)

    new_cookies = response.headers.get('Set-Cookie', "").split(";")
    session_id = None
    for cookie in new_cookies:
        cookie_name_value = cookie.split("=")
        if cookie_name_value[0] == "BREEZESESSION":
            session_id = cookie_name_value[-1]

    if session_id is None:
        print("Session id not found.")
        exit()

    return session_id


def get_user_pass():
    with open("lms_auth.txt", "a+") as f:
        f.seek(0)
        line = f.readline().strip()
        if ":" in line:
            username, password = line.split(":")
            if not (username == "username" and password == "password"):
                return username, password
        else:
            f.write("username:password")
 
        print(
            "\n\033[93mPlease replace username and password in lms_auth.txt with you lms user pass.\033[0m")
        exit()


if __name__ == "__main__":
    username, password = get_user_pass()
    class_id, class_name = uni_classes["computer_architecture"].values()

    join_a_class(username, password, class_id, class_name)
    input("Press enter to leave the class.")
