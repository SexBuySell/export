import urllib.request
import lxml.etree as ET
import logging
import os

# Налаштування логування
logging.basicConfig(
    filename='script_log.log',  
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# URL прайс-листу
url = "https://smtm.com.ua/_prices/import-retail-2.xml"

try:
    # Завантаження XML
    response = urllib.request.urlopen(url)

    # Перевірка на успішне завантаження
    if response.status == 200:
        # Розбір XML
        content = response.read()
        root = ET.fromstring(content)

        # Список категорій, які потрібно видалити
        categories_to_delete = [...]  # твої категорії

        # Пройдемося по кожному <offer> елементу і видалимо його, якщо категорія в списку categories_to_delete
        for offer in root.xpath('//offer'):
            category_element = offer.find('.//categoryId')
            if category_element is not None and category_element.text in categories_to_delete:
                offer.getparent().remove(offer)

        # Запишемо оновлений XML у файл
        with open('import.xml', 'wb') as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
            file.write(ET.tostring(root, encoding='utf-8'))

        logging.info('Скрипт виконано успішно')
        
        # Додано: перевірка змісту файлу
        logging.info(f'Файл import.xml перезаписано. Вміст:\n{ET.tostring(root, encoding="utf-8").decode("utf-8")}')
    else:
        logging.error(f'Помилка при завантаженні: {response.status}')
except Exception as e:
    logging.error(f'Помилка: {e}')
