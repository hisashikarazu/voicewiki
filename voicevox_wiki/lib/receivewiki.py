import re


from selenium import webdriver
from selenium.webdriver.common.by import By


from lib import text2wav


def text_replace(text_list: list) -> list:
    dc1 = '\[.+?\]| '
    dc2 = '-'

    t_list = []
    for s in text_list:
        t_list.append(re.sub(dc1, '', s).replace(dc2, '、'))

    return t_list


def from_wiki(text_length_type: int = 0):

    wiki_url = """
    https://ja.wikipedia.org/wiki/Wikipedia:%E
    4%BB%8A%E6%97%A5%E3%81%AF%E4%BD%95%E3%81%AE%E6%97%A5
    """
    delete_char = r'\n|\s'
    wiki_url = re.sub(delete_char, '', wiki_url)

    driver = webdriver.Chrome()
    driver.get(wiki_url)
    driver.implicitly_wait(10)

    #日付け取得
    date = text2wav.this_date(1)
    
    this_month = driver.find_element(by=By.LINK_TEXT, value=date[0])
    this_month.click()


    wday_list = []
    #簡素
    if text_length_type == 0:
        date_int = text2wav.this_date(2)
        xpath_this_d = f'//*[@id="mw-content-text"]/div[1]/ul[{date_int[1]}]'
        this_d = driver.find_elements(by=By.XPATH, value=xpath_this_d)
        d_list = this_d[0].text.split('\n')

    #長い
    elif text_length_type == 1:
        date_s = text2wav.this_date()

        date_hylink = driver.find_element(by=By.LINK_TEXT, value=date_s)
        date_hylink.click()

        xpath_subject = '//*[@id="できごと"]'
        sub_name = driver.find_element(by=By.XPATH, value=xpath_subject)

        xpath_this_d = f'//*[@id="mw-content-text"]/div[1]/ul[1]'
        this_d = driver.find_elements(by=By.XPATH, value=xpath_this_d)
        d_list = this_d[0].text.split('\n')
        
        d_list = text_replace(d_list)

        #from_wiki_preとの型合わせ: こちらのみ
        wday_list = [f'今日は何の日 {text2wav.this_date()}']

        print(sub_name.text)

    else:
        return None

    
    wday_list.extend(d_list)

    url = driver.current_url
    driver.quit()

    return wday_list, url, text_length_type


def from_wiki_pre():
    wiki_url = """
    https://ja.wikipedia.org/wiki/%E3%83%A1%E
    3%82%A4%E3%83%B3%E3%83%9A%E3%83%BC%E3%82%B8
    """
    delete_char = r'\n|\s'
    wiki_url = re.sub(delete_char, '', wiki_url)

    driver = webdriver.Chrome()
    driver.get(wiki_url)
    driver.implicitly_wait(10)

    wday = driver.find_elements(by=By.ID, value='on_this_day')
    wday_list = wday[0].text.split('\n')

    u = driver.find_element(by=By.LINK_TEXT, value='今日は何の日')
    u.click()

    url = driver.current_url
    driver.quit()

    return wday_list, url