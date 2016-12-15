from driver import Driver
import time
from selenium.webdriver.common.keys import Keys
from core.models import News


def publish_news(news_id, add_link=True, add_content=True):
    news = News.objects.get(pk=news_id)
    link = news.link
    content = news.content
    driver = Driver("firefox", False, headless=True).driver
    driver.get("http://vk.com")
    elem_email = driver.find_element_by_id('index_email')
    elem_password = driver.find_element_by_id('index_pass')
    elem_email.send_keys('')
    elem_password.send_keys('')
    elem_submit = driver.find_element_by_id('index_login_button')
    elem_submit.click()
    time.sleep(3)

    driver.get('https://vk.com/programmersnews')
    time.sleep(3)
    add_news_field = driver.find_element_by_css_selector('#post_field')
    if add_link:
        add_news_field.send_keys(link)
        time.sleep(2)
        add_news_field.send_keys(Keys.ENTER)
        time.sleep(2)
    if add_content:
        add_news_field.send_keys(content)
        time.sleep(2)
    send_post = driver.find_element_by_css_selector("#send_post")
    send_post.click()
    time.sleep(2)
    driver.close()