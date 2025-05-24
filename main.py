import logging, coloredlogs
import time
import json
import logging, coloredlogs
import pandas as pd
import openpyxl
import undetected_chromedriver as uc
from colorama import Fore, Back, Style, init
from pyfiglet import Figlet
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

LOG_FORMAT = '[%(asctime)s] [%(name)s] [%(funcName)s:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
LOG_LEVEL = logging.INFO
LOG_STYLES = {
    'debug': {'color': 'blue'},
    'info': {'color': 'white'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'bold': True, 'color': 'red'},
    'success': {'bold': True, 'color': 'green'},
    'verbose': {'color': 'blue'},
    'notice': {'color': 'magenta'}
}
logger = logging.getLogger('pl-dl')
coloredlogs.install(level=LOG_LEVEL, logger=logger, fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT, level_styles=LOG_STYLES)

init(autoreset=True) # Para restablecer colores después de cada impresión 
font = Figlet(font='slant')
script_title = 'Scraping-test'
print(Fore.GREEN + Style.BRIGHT + font.renderText(script_title))
print(Back.GREEN + Style.BRIGHT + "scraping-test")
print()

options = Options()
options.add_argument('--incognito')
options.add_argument('--disable-blink-features=AutomationControlled')

# Inicia el navegador
driver =  webdriver.Chrome(options=options)
driver.maximize_window()

url = "https://platzi.com/agenda/"
driver.get(url) 
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")
#print(soup.prettify())

course_list = []

last_courses = soup.find_all('section', id = 'row-last-courses')

for detail in last_courses:
    course_title = detail.find_all('span', class_= 'RowDate-detailCopy') 
    for title in course_title:
        course_list.append(title.text.strip())

# print(json.dumps(course, indent=4, ensure_ascii= False))

#Guardar la lista en un DataFrame de pandas
if course_list:
    df = pd.DataFrame(course_list)

    # Guardar el DataFrame en un archivo Excel
    excel_filename = "lista_cursos.xlsx"
    df.to_excel(excel_filename, index=False, sheet_name="agenda", header=['Cursos de la agenda'])
    logger.info(f"La lista de cursos se guardado en el archivo: {excel_filename}")
else:
    logger.warning("No se encontraron cursos para guardar.")


# Guardar el contenido en un archivo .txt
# with open('lista_cursos.txt', 'a', encoding='utf-8') as file:
#     for title in course_list:
#         course = title.text.strip()
#         file.write(course+'\n') 








 
