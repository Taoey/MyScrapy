from selenium import webdriver

if __name__ == '__main__':
    browser = webdriver.Firefox()
    browser.get('https://leetcode-cn.com/problems/binary-watch/description/')
    print(browser.page_source)

