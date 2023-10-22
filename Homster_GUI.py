
import tkinter as tk
from tkinter import *
from bs4 import BeautifulSoup
import requests
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import csv
import pandas as pd
from pandas import DataFrame
import numbers
import random
import numpy as np
from time import sleep
import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from datetime import date, datetime
import os, sys
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


ROOT = tk.Tk()
ROOT.geometry("400x200")

ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="Parse Krisha.kz for search",
                                  prompt="Enter URL")

url = USER_INP

#PATH_CHROMEDRIVER = askopenfilename()
#pathway_chromediriver = PATH_CHROMEDRIVER
driver = webdriver.Chrome()

driver.get(url)




#Pagination

pages = driver.find_elements(By.CLASS_NAME, 'b-pagination__item')[-2]


last_page = int(pages.get_attribute('data-page'))


url_split = url.split('&page=1')
url1 = url_split [0]
url2 = url_split [1]
url_list = []

for x in range(1,last_page+1):
    url_sum = url1 + '&page=' + str(x) + url2
    url_list.append(url_sum)

print (last_page)
print(url_list)





#Get links

raw_links = []
raw_name_data = []
raw_price = []

driver.implicitly_wait(1)

for page in url_list:
    current_url = page 
    driver.get(current_url)
    link_data = driver.find_elements(By.CLASS_NAME, 'b-snippet__link__complexSnippetServer')
    
    
    for links in link_data:
        link_data = links.get_attribute('href')
        name_data = links.get_attribute('data-name')
        price_data = links.get_attribute('data-name')
        raw_links.append(link_data)
        raw_name_data.append(name_data)
    

   





#Core data parsing

filtered_links = []
filtered_names = []


for filter in raw_links:
    if filter != None :
        filtered_links.append(filter)

for filter in raw_name_data:
    if filter !=None :
        filtered_names.append(filter)



dict_names = list(dict.fromkeys(filtered_names)) 
dict_links = list(dict.fromkeys(filtered_links)) 


test_links = dict_links[0:4]

print(len(dict_names))
print(dict_links)





# Raw data parsing block

link_data = []
price_data = []

company_data = []
city_data = []
district_data = []
address_data = []
full_ad_data = []
status_data = []
amount_data = []
available_data = []
sqm_data = []
deadline_data = []
class_data = []
decor_data = []
parking_data =[]
floors_data = []
height_data = []
type_data = []
extra_data = []

#min_price_data = []
#max_price_data = []
# one_data = []
# two_data = []
# three_data = []
# four_data = []
# fourplus_data = []
# 
# one_data_sq = []
# two_data_sq = []
# three_data_sq = []
# four_data_sq = []
# fourplus_data_sq = []
# 
# one_data_price = []
# two_data_price = []
# three_data_price = []
# four_data_price = []
# fourplus_data_price = []


for selection in dict_links:
    
    sleep(1)
    try:
        driver.implicitly_wait(0)
        driver.get(selection)
    
        
    
        link_data.append(selection)
    
        try:

             company = driver.find_element(By.XPATH, '//*[@id="developer-details"]/div[2]/div[2]/div[1]/a').text
    
        except Exception as _ex:
        
             company = None
             
        company_data.append(company)
        
    
        try:
             price = driver.find_element(By.CLASS_NAME, 'b-complex-block__sub-title').text
    
    
        except Exception as _ex:
        
             price = 'Продажи завершены'
        
        price_data.append(price)
    
        try: 
             full_adress = driver.find_element(By.CLASS_NAME, 'b-complex-heading-info__sub-title').text
             raw_adress = full_adress.split(',')
             if raw_adress[0] == 'Казахстан':
                    city = raw_adress[1]
                    district = raw_adress[2]
                    try:
                        street = str(raw_adress[3:]).replace('[','').replace(']','').replace("'","")
                        if 'район' not in district:
                            street = str(raw_adress[1:]).replace('[','').replace(']','').replace("'","")
                            district = None
                            
                    except: 
                        street = None
             else:
                    city = raw_adress[0]
                    district = raw_adress[1]
                    try:
                        street = str(raw_adress[2:]).replace('[','').replace(']','').replace("'","")
                        if 'район' not in district:
                            district = None
                            street = str(raw_adress[1:]).replace('[','').replace(']','').replace("'","")
                    except: 
                        street = None

        except Exception as _ex:
             full_adress = None
        
        
        full_ad_data.append(full_adress)
        city_data.append(city)
        district_data.append(district)
        address_data.append(street)

        try:
                sqm_raw = driver.find_element(By.XPATH, '//*[@id="other-offers"]/div[2]/div[2]/div[1]/a[1]/div[2]/div[2]/span[2]').text
                sqm_r = str(sqm_raw).replace('от','').replace('тыс тг/м²', '').replace('*','')
                sqm = float(str(sqm_r.replace(',','.'))) * 1000
                    
        except Exception as _ex:
                sqm = 'Не указано'


        sqm_data.append(sqm)
     
        decor = None
        deadline = ''
        class_ = ''
        floor = None
        amount = None
        parking = None
        height = None
        type = None
        status = None
    
    
        #Block 1
        
        for i in range(1,16):
               
            try: 
                    xpath = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Отделка': 
                        decor = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        decor = None
    
            except:
                    pass
                
        decor_data.append(decor)  
    
    
        for i in range(1,16):
                
            try:    
                    
                    xpath = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Сдача': 
                        deadline = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        deadline = 'Не указан'
    
            except:
                    pass
                
        deadline_data.append(deadline)  
    
    
    
        for i in range(1,16):
                
            try: 
                    xpath = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Класс жилья*': 
                        class_ = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        class_ = 'Не указан'
    
            except:
                    pass
                
        class_data.append(class_)  
    
    
    
        for i in range(1,16):
                
            try: 
                    xpath = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Кол-во этажей': 
                        floor = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        floor = None
    
            except:
                    pass
                
        floors_data.append(floor)  
    
    
    
    
        for i in range(1,16):
                
            try: 
                    xpath = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Количество объектов': 
                        amount = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        amount = None
    
            except:
                    pass
                
        amount_data.append(amount)  
    
    
    
        for i in range(1,16):
                
            try: 
                    xpath = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[1]/div[' + str(i) + ']/div[2]/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Этап строительства': 
                        status = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        status = None
    
            except:
                    pass
                
        status_data.append(status)  
    
    
    
    
        #Block 2 ______________
    
        for i in range(1,16):
                
            try: 
                    xpath = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Квартир в продаже': 
                        available = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        available = None
    
            except:
                    pass
                
        available_data.append(available)  
    
    
    
        for i in range(1,16):
                
            try: 
                    xpath = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[2]'
                    check = driver.find_element(By.XPATH, xpath).text
                    if check == 'Паркинг': 
                        parking = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        parking = None
    
            except:
                    pass
                
        parking_data.append(parking)  
    
        for i in range(1,16):
            try:
            
                    xpath = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[2]'
                    check = driver.find_element(By.XPATH, xpath ).text
                    if check == 'Высота потолка':
                        height = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        height = None
            except:
                    pass
                
                
        height_data.append(height)
    
        for i in range(1,16):
            try:
            
                    xpath = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[1]'
                    correct = '//*[@id="parameters"]/div[2]/div[2]/div[' +str(i) + ']/span[2]'
                    check = driver.find_element(By.XPATH, xpath ).text
                    if check == 'Тип здания':
                        type = driver.find_element(By.XPATH, correct).text
                        break
                    else:
                        type = None
            except:
                    pass
                
                
        type_data.append(type)
        
    
        # BLOCK 3
        raw_extra_data = []
        for i in range(1,16):
        
            try:
                xpath = '//*[@id="parameters"]/div[2]/div[3]/div[' + str(i) + ']/div'
                check = driver.find_element(By.XPATH, xpath ).text
                check_str = str(check).replace('[','').replace(']','').replace("'","")
                raw_extra_data.append(check_str)
                if check == '' or None:
                    break
            except:
                    pass
                
                
        extra_data.append(raw_extra_data)  


    except:
        pass

       

     

          
          

         
     

     




# Data cleaning block

class_data = list(map(lambda x: x.replace('I (Элит)', 'Элит'), class_data))
class_data = list(map(lambda x: x.replace('II (Бизнес)', 'Бизнес'), class_data))
class_data = list(map(lambda x: x.replace('III (Комфорт)', 'Комфорт'), class_data))
class_data = list(map(lambda x: x.replace('IV (Эконом)', 'Эконом'), class_data))

deadline_data = list(map(lambda x: x.replace('I', '1'), deadline_data))
deadline_data = list(map(lambda x: x.replace('11', '2'), deadline_data))
deadline_data = list(map(lambda x: x.replace('111', '3'), deadline_data))
deadline_data = list(map(lambda x: x.replace('1V', '4'), deadline_data))




# Price corretion block

unfiltered_price_data = []
new_list = []
mod_list = []
min_list = []
max_list = []
filtered_available_data = []
filtered_amount_data = []

for i in price_data:
    min_price = re.findall("\d+\,\d+", str(i))
    unfiltered_price_data.append(min_price)

#for i in unfiltered_price_data:
#    digit = str(i).replace(',','.')
#    new_list.append(digit)
#
#for i in new_list:
#    price = re.findall('\d+.\d+', str(i))
#    mod_list.append(price)



for i in unfiltered_price_data:
    try: 
        min_value = float(str(min(i)).replace(',','.'))* 1000000
        max_value = float(str(max(i)).replace(',','.')) * 1000000
    except Exception as _ex:
        min_value = 'Продажи Завершены'
        max_value = 'Продажи Завершены'

    min_list.append(min_value)
    max_list.append(max_value)

datacheck = [dict_links, dict_names, min_list, max_list, sqm_data, company_data, city_data, district_data, address_data, full_ad_data, status_data, amount_data, available_data, deadline_data, height_data, floors_data, parking_data, decor_data, class_data, type_data, extra_data]

for i in datacheck:
    print (len(i))

#for j in datacheck:
#   print (j)

df  = DataFrame (
    
{
    'Ссылка' : dict_links,
    'Название' : dict_names,
    'Минимальная цена' : min_list,
    'Максимальная цена' : max_list, 
    'Цена за квадрат' : sqm_data,
    'Застройщик': company_data, 
    'Город' : city_data,
    'Район' : district_data,
    'Улица' : address_data,
    'Адрес' : full_ad_data,
    'Статус' : status_data,
    'Всего квартир' : amount_data,
    'Доступно квартир' : available_data,
    'Дедлайн' : deadline_data,
    'Высота потолков' : height_data,
    'Этажность' : floors_data,
    'Паркинг' : parking_data,
    'Отделка' : decor_data,
    'Класс' : class_data,
    'Тип' : type_data, 
    'Доп' : extra_data
    

}

)

filename = asksaveasfilename()
df.to_excel(filename + '.xlsx')



