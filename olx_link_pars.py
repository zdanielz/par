from bs4 import BeautifulSoup
import re
import requests
import json


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
i = 0


file = open("./data/links.txt", "r")
links = file.readlines()
link_number = 0
data = []

for i in range(len(links)):
    links[i] = links[i][0:-1]
    i += 1


while link_number < 2:

    offer_details_name = []
    offer_details_value = []

    requests_dat = requests.get(links[link_number], headers=headers)

    html_l = requests_dat.content.decode("utf-8")
    cookies = requests_dat.cookies

    offer_details_name_raw = BeautifulSoup(html_l, 'lxml').find("ul", {"class": "offer-details"}).find_all("span", {"class": "offer-details__name"})
    offer_details_value_raw = BeautifulSoup(html_l, 'lxml').find("ul", {"class": "offer-details"}).find_all("strong", {"class": "offer-details__value"})
    description = "Описание: " + str(BeautifulSoup(html_l, 'lxml').find("div", {"class": "descriptioncontent"}).find("div", {"id": "textContent"}).text.replace("   ", "").replace("\r", "").replace("\n", ""))

    ob_id_tag = BeautifulSoup(html_l, 'lxml').find("div", {"class": "contact-button"})

    pattern = re.compile('\'id\':(\'.*?\'),')
    ob_id = re.findall(pattern, str(ob_id_tag))[0][1:-1]

    pattern = re.compile('var phoneToken = (\'.*?\');')
    phoneToken = re.findall(pattern, str(html_l))[0][1:-1]

    print(ob_id)
    print(phoneToken)
    print(cookies)

    phone = requests.get("https://www.olx.ua/ajax/misc/contact/phone/{0}/?pt={1}".format(ob_id, phoneToken), headers=headers, cookies=cookies).content
    print(phone)

    for i in range(len(offer_details_name)):
        data.append("{0}: {1}".format(offer_details_name_raw[i].text, offer_details_value_raw[i].text))

    data.append(description)

    with open("./data/links_data/link_" + str(link_number) + "_data" + '.json', 'w') as f:
        json.dump(data, f)

    link_number += 1
