from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import shutil

not_found = False
page_number = 1
coins_dir = os.path.dirname(os.path.realpath(__file__)) + '/coins'

while not_found is False:
    soup = BeautifulSoup(urlopen('https://coinmarketcap.com/{page}'.format(page=page_number)), 'html.parser')

    if len(soup.select('.title-404')) > 0:
        print('No more pages.')
        break

    images = soup.select('.currency-name img')
    for image in images:
        coin_name = image.get('alt')
        file_name = '{coins_dir}/{coin_name}/logo.png'.format(coins_dir=coins_dir, coin_name=coin_name)
        url = image.get('data-src') or image.get('src')
        coin_path = '{coins_dir}/{coin_name}'.format(coins_dir=coins_dir, coin_name=coin_name)
        if not os.path.exists(coin_path):
            os.makedirs(coin_path)
        print('Downloading {coin}'.format(coin=coin_name))

        with urlopen(url) as response, open(file_name, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

    page_number += 1
    print('Switching to page {page}'.format(page=page_number))


