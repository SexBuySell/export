import urllib.request
import lxml.etree as ET
import logging
import os

# Отримуємо поточну робочу директорію з $GITHUB_WORKSPACE
workspace = os.getenv('GITHUB_WORKSPACE', '.')

# Налаштування логування без мілісекунд, вказуємо шлях до логу
log_file_path = os.path.join(workspace, 'script_log.log')
logging.basicConfig(
    filename=log_file_path,
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
        logging.info('XML файл успішно завантажено.')
        
        # Розбір XML
        content = response.read()
        root = ET.fromstring(content)

        # Список категорій, які потрібно видалити
        categories_to_delete = ['6533', '6534', '6535', '4848', '4917', '2621', '4799', '4801', '10', '5467', '4860', '4898', '4899', '4900', '4901', '7029', '9698', '4866', '4870', '4882', '4883', '4893', '4894', '4906', '4902', '4903', '4904', '4905', '5461', '8203', '5302', '4794', '4797', '8181', '15080', '17831', '9495', '9496', '4878', '4880', '2316']

        deleted_offers_count = 0  # Лічильник видалених елементів
        # Пройдемося по кожному <offer> елементу і видалимо його, якщо категорія в списку categories_to_delete
        for offer in root.xpath('//offer'):
            category_element = offer.find('.//categoryId')
            if category_element is not None and category_element.text in categories_to_delete:
                offer.getparent().remove(offer)
                deleted_offers_count += 1

        if deleted_offers_count > 0:
            logging.info(f'Видалено {deleted_offers_count} елементів.')
        else:
            logging.info('Не було видалено жодного елемента.')

        # Запишемо оновлений XML у файл
        output_file_path = os.path.join(workspace, 'import.xml')
        with open(output_file_path, 'wb') as new_price_list:
            new_price_list.write('<?xml version="1.0" encoding="UTF-8"?>\n'.encode('utf-8'))
            new_price_list.write(ET.tostring(root, encoding='utf-8'))

        logging.info('Скрипт виконано успішно, файл import.xml оновлено.')
    else:
        logging.error(f'Помилка при завантаженні: {response.status}')
except Exception as e:
    logging.error(f'Помилка: {e}')
