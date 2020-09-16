from selenium import webdriver
import time

url = "https://auth.alipay.com/login/index.htm"
name =""
password = ''
def login():
    browser = webdriver.Firefox()
    browser.get(url)

    browser.find_elements_by_xpath("//*[@id='J-loginMethod-tabs']/li[2]")[0].click()
    name_box = browser.find_elements_by_xpath('//*[@id="J-input-user"]')[0]

    for i in name:
        name_box.send_keys(i)
        time.sleep(0.5)

    password_box = browser.find_elements_by_xpath('//*[@id="password_rsainput"]')[0]
    for i in password:
        password_box.send_keys(i)
        time.sleep(0.5)

    #登录
    browser.find_elements_by_xpath('//*[@id="J-login-btn"]')[0].click()

    login_flag = False

    while login_flag == False:
        try:
            #进入账单页面
            browser.find_elements_by_xpath('//*[@id="globalContainer"]/div[2]/div/div[1]/div/ul/li[2]/a')[0].click()
            login_flag = True
            print("登录成功")
        except:
            print("等待登录")

    print(browser.page_source)
    browser.close()
    return 0

def getData():
    return 0


if __name__ == '__main__':
    login()