import math
import os
import re
import sys
import time
import requests
from bs4 import BeautifulSoup

from pyquery import PyQuery as pq

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django

django.setup()


def getProducts(url, lastPage=3, limitPages=11):
    products = []

    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features="lxml")

    # dom = pq(response)

    for i in range(1, lastPage + 1):
        page = url + "/p" + str(i)
        if i > 1:
            r = requests.get(page).text
            try:
                dom = pq(r)
            except:
                return products

        rawProducts = soup.findAll(True, {"class": ["js-product-data"]})
        # rawReviews = soup.find('div[data-component-type]')

        for rawProduct in reversed(rawProducts):
            details = {}
            content = rawProduct.get_text()

            details["productDataDiscovered"] = int(time.time())
            details["productLink"] = rawProduct.find_all("div", {"class": "card-v2-info"})[0].contents[0].attrs['href']
            details["productTitle"] = rawProduct.attrs['data-name']
            details["productCategory"] = rawProduct.attrs['data-category-trail']
            details["productPrice"] = rawProduct.find_all("p", {"class": "product-new-price"})[0].text
            details["productImg"] = rawProduct.find_all("div", {"class": "card-v2-info"})[0].contents[0].contents[0].attrs['src']
            # details['productReview'] = rawProduct.find_all("span", {"class": "average-rating semibold"})[0].text

            products.append(details)

        print('page {}/{} {} reviews'.format(i, lastPage, len(products)), flush=True)
        if i >= limitPages:
            break

    return products


def checkUrl(url):
    if re.search("(www\.emag\.ro.*?)", url):
        return True
    else:
        return False


if __name__ == '__main__':
    url = "https://www.emag.ro/search/iphone"
    print(checkUrl(url))
    products = getProducts(url)
    print(products)
    print(len(products))
