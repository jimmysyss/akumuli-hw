import csv
import os
import re

import jinja2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.binary_location = '/usr/bin/chromium-browser'
chrome_options.binary = '/usr/lib/chromium-browser/chromium-browser'
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"/home/jimmy/Workspaces-Pycharm/timeseries/data",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

download_list = ['http://10.0.0.162/datamodel/201809a/auth/Tables.html']


def camel_case(column_name):
    return re.sub('_([a-z])', lambda match: match.group(1).upper(), column_name.lower())


def Camel_case(column_name):
    camel_case_name = camel_case(column_name)
    return camel_case_name[:1].upper() + camel_case_name[1:]


def download():
    for site in download_list:
        try:
            driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),
                                      chrome_options=chrome_options)
            driver.get(site)

            # Retrieve a list of tables on the left
            tablename_sections = driver.find_elements_by_xpath("//*[contains(@id, 'Table_')]")
            # list(map(lambda element: print(element.find_element_by_class_name('caption1').text), tablename_sections))

            for table_element in tablename_sections:
                # Column information
                col_elements = table_element.find_elements_by_xpath('.//table[3]/tbody/*')
                col_list = []
                for col_element in col_elements:
                    tds = col_element.find_elements_by_class_name('tabdata')

                    if len(tds)>0:
                        col_def = {
                            "pk": (tds[0].text == 'PK'),
                            "field_name": tds[1].text,
                            "domain": tds[2].text,
                            "data_type": tds[3].text,
                            "not_null": (tds[4].text == 'YES'),
                            "unique": (tds[5].text == 'YES'),
                            "check": (tds[6].text == 'YES'),
                            "default": tds[7].text if (tds[7].text != '') else None,
                            "comments": tds[8].text,
                        }
                        col_list.append(col_def)

                # Key Information
                key_elements = table_element.find_elements_by_xpath('.//table[4]/tbody/*')
                key_list = []
                for key_element in key_elements:
                    tds = key_element.find_elements_by_class_name('tabdata')

                    if len(tds)>0:
                        key_def = {
                            "key_type": tds[0].text,
                            "key_name": tds[1].text,
                            "domain": tds[2].text,
                        }
                        key_list.append(key_def)

                table = {
                    "table_name": table_element.find_element_by_class_name('caption1').text,
                    "col_list": col_list,
                    "key_list": key_list
                }

                print(table)
                class_content = env.get_template('entity.template').render(table)

                # Write to file
                with open("class/%s.java" % Camel_case(table['table_name']), "w") as text_file:
                    print(re.sub(r"\s{3,}", "\r\n\r\n", class_content), file=text_file)

            driver.close()
        except Exception as e:
            print(e)
        else:
            pass

    #
    # with open('hkstock.csv', 'r') as csv_file:
    #     reader = csv.DictReader(csv_file, delimiter=',')
    #
    #     for row in reader:
    #         stock_code = row['stock']
    #         print(stock_code)
    #
    #         try:
    #             driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),
    #                                       chrome_options=chrome_options)
    #             driver.get("https://finance.yahoo.com/quote/{}/history?p={}".format(stock_code, stock_code))
    #             time_period_field = driver.find_element_by_xpath(
    #                 '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/span/input')
    #             webdriver.ActionChains(driver).move_to_element(time_period_field).pause(3).click(
    #                 time_period_field).perform()
    #
    #             max_button = driver.find_element_by_xpath(
    #                 '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[1]/span[8]/span')
    #             webdriver.ActionChains(driver).move_to_element(max_button).pause(3).click(
    #                 max_button).perform()
    #
    #             done_button = driver.find_element_by_xpath(
    #                 '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/span[2]/div/div[3]/button[1]')
    #             webdriver.ActionChains(driver).move_to_element(done_button).pause(3).click(
    #                 done_button).perform()
    #
    #             apply_button = driver.find_element_by_xpath(
    #                 '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button')
    #             webdriver.ActionChains(driver).move_to_element(apply_button).pause(3).click(
    #                 apply_button).pause(3).perform()
    #
    #             download_button = driver.find_element_by_xpath(
    #                 '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')
    #             webdriver.ActionChains(driver).move_to_element(download_button).click(
    #                 download_button).perform()
    #
    #             webdriver.ActionChains(driver).pause(7).perform()
    #
    #             driver.close()
    #         except Exception as e:
    #             print(e)
    #         else:
    #             pass


env = jinja2.Environment(loader=jinja2.FileSystemLoader(''))
env.globals['camel_case'] = camel_case
env.globals['Camel_case'] = Camel_case
if __name__ == '__main__':
    download()
