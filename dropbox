import urllib.request
import lxml.etree as ET
import dropbox
import datetime
import os
from dotenv import load_dotenv

# Завантажити змінні з .env
load_dotenv()

# Функція для запису логів
def write_log(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} - {message}\n"
    with open('log.txt', 'a') as log_file:
        log_file.write(log_message)

# Створюємо папку upload, якщо вона не існує
upload_folder = 'upload'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

# URL прайс-листу
url = "https://smtm.com.ua/_prices/import-retail-2.xml"

# Ваш Access Token для Dropbox з .env файлу
access_token = os.getenv('DROPBOX_ACCESS_TOKEN')
dbx = dropbox.Dropbox(access_token)

try:
    write_log("Запуск скрипта.")
    
    # Завантаження XML
    response = urllib.request.urlopen(url)

    # Перевірка на успішне завантаження
    if response.status == 200:
        # Розбір XML
        content = response.read()
        root = ET.fromstring(content)

        # Список категорій, які потрібно видалити
        categories_to_delete = ['6533', '6534', '6535', '4848', '4917', '2621', '4799', '4801', '10', '5467', '4860', 
                                '4898', '4899', '4900', '4901', '7029', '9698', '4866', '4870', '4882', '4883', '4893', 
                                '4894', '4906', '4902', '4903', '4904', '4905', '5461', '8203', '5302', '4794', '4797', 
                                '8181', '15080', '17831', '9495', '9496', '4878', '4880', '2316']

        # Видалення категорій
        for offer in root.xpath('//offer'):
            category_element = offer.find('.//categoryId')
            if category_element is not None and category_element.text in categories_to_delete:
                offer.getparent().remove(offer)

        # Змінюємо місце збереження файлу
        local_file_path = os.path.join(upload_folder, 'import.xml')
        with open(local_file_path, 'wb') as new_price_list:
            new_price_list.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
            new_price_list.write(ET.tostring(root, encoding='utf-8'))

        # Завантаження файлу на Dropbox
        with open(local_file_path, 'rb') as f:
            dbx.files_upload(f.read(), '/import.xml', mode=dropbox.files.WriteMode.overwrite)

        write_log(f"Файл 'import.xml' успішно створено у папці '{upload_folder}' та завантажено на Dropbox.")
    else:
        error_message = f'Помилка при завантаженні: {response.status}'
        write_log(error_message)
        print(error_message)

except Exception as e:
    error_message = f'Помилка: {e}'
    write_log(error_message)
    print(error_message)

# Завантаження лог-файлу на Dropbox
with open('log.txt', 'rb') as log_file:
    dbx.files_upload(log_file.read(), '/log.txt', mode=dropbox.files.WriteMode.overwrite)
