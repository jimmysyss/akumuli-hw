import csv
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.binary_location = '/usr/bin/chromium-browser'
chrome_options.binary = '/usr/lib/chromium-browser/chromium-browser'
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"/home/jimmy/Workspaces-Pycharm/timeseries/data",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})


def download():
    with open('hkstock.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')

        for row in reader:
            stock_code = row['stock']
            print(stock_code)

            try:
                driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
                driver.get("https://finance.yahoo.com/quote/{}/history?p={}".format(stock_code, stock_code))
                time_period_field = driver.find_element_by_xpath(
                    '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input')
                webdriver.ActionChains(driver).move_to_element(time_period_field).pause(3).click(
                    time_period_field).perform()

                max_button = driver.find_element_by_xpath(
                    '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[1]/span[8]/span')
                webdriver.ActionChains(driver).move_to_element(max_button).pause(3).click(
                    max_button).perform()

                done_button = driver.find_element_by_xpath(
                    '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]')
                webdriver.ActionChains(driver).move_to_element(done_button).pause(3).click(
                    done_button).perform()

                apply_button = driver.find_element_by_xpath(
                    '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
                webdriver.ActionChains(driver).move_to_element(apply_button).pause(3).click(
                    apply_button).pause(3).perform()

                download_button = driver.find_element_by_xpath(
                    '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
                webdriver.ActionChains(driver).move_to_element(download_button).click(
                    download_button).pause(5).perform()

                driver.close()
            except Exception as e:
                print(e)
            else:
                pass



if __name__ == '__main__':
    download()
