from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import time
import os

GAIA_URL = "https://www.gaiagps.com/datasummary/photos/"
GAIA_PHOTO_API = "https://www.gaiagps.com/api/objects/photo/"

def save_images(images_to_parse):
    if not images_to_parse:
        print('All images processed')
        return
    else:
        url = images_to_parse[0]['url']
        name = images_to_parse[0]['name']
        print('Processing image', name)
        driver.get(url)
        #time.sleep(2)
        urllib.request.urlretrieve(driver.current_url, 'gaia/' + name + ".jpg")
        save_images(images_to_parse[1:])


def get_images(count = 0):
    images = driver.find_elements_by_xpath(
        "//a[starts-with(@href, '" + GAIA_PHOTO_API + "')]")
    if not images:
        'No images on page'
        return
    else:
        image_count = len(images)

        images_to_parse = [
            {
                'url': images[i].get_attribute('href').replace('/1000/','/full/'),
                'name': str(i + count)
            }
            for i in range(image_count)
        ]
        driver.switch_to.window(window_after)
        time.sleep(2)

        save_images(images_to_parse)

        driver.switch_to.window(window_before)
        time.sleep(2)

        next_button = driver.find_element_by_link_text('Next')
        if 'disabled' in next_button.find_element_by_xpath('..').get_attribute("class"):
            print("We're done folks!")
            return

        print("Next Page!")
        next_button.click()
        time.sleep(1)
        get_images(count + image_count)



driver = webdriver.Firefox()
driver.get(GAIA_URL)

email_value = input('Email: ')
password_value = input('Password: ')

email_field = driver.find_element_by_id("login-email")
password_field = driver.find_element_by_id("login-password")

email_field.send_keys(email_value)
password_field.send_keys(password_value)
driver.find_element_by_xpath("//button[@type='submit']").click()

time.sleep(2)
window_before = driver.window_handles[0]
driver.execute_script("window.open('" + GAIA_URL + "', 'new window')")
window_after = driver.window_handles[1]
driver.switch_to.window(window_before)
time.sleep(2)

if not os.path.exists('gaia'):
    os.makedirs('gaia')

time.sleep(2)
get_images()
