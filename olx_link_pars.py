from bs4 import BeautifulSoup
import re
import requests
import json
from itertools import groupby
import random
import time


def link_parser(proxy_list, use_proxy):

    time_start = time.time()

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    file = open("./data/links.txt", "r")
    links = file.readlines()
    link_number = 0
    data = {}

    for i in range(len(links)):
        links[i] = links[i][0:-1]
        i += 1

    while link_number < 21:
        phone_hide_type = 0

        start_one_link_time = time.time()

        headers.update({"referer": links[link_number]})

        if use_proxy == True:
            requests_dat = requests.get(links[link_number], headers=headers, proxies=random.choice(proxy_list))
        elif use_proxy == False:
            requests_dat = requests.get(links[link_number], headers=headers)

        html_l = requests_dat.content.decode("utf-8")
        cookies = requests_dat.cookies

        offer_details_name_raw = BeautifulSoup(html_l, 'lxml').find("ul", {"class": "offer-details"}).find_all("span", {"class": "offer-details__name"})
        offer_details_value_raw = BeautifulSoup(html_l, 'lxml').find("ul", {"class": "offer-details"}).find_all("strong", {"class": "offer-details__value"})
        description = "Описание: " + str(BeautifulSoup(html_l, 'lxml').find("div", {"class": "descriptioncontent"}).find("div", {"id": "textContent"}).text.replace("   ", "").replace("\r", "").replace("\n", ""))

        try:
            ob_id_tag = BeautifulSoup(html_l, 'lxml').find("div", {"class": "contact-button"})

            pattern = re.compile('\'id\':(\'.*?\'),')
            ob_id = re.findall(pattern, str(ob_id_tag))[0][1:-1]
        except IndexError:
            ob_id_tag = BeautifulSoup(html_l, 'lxml').find("span", {"class": "spoilerHidden"})

            pattern = re.compile('data-id=(\".*?\") ')
            ob_id = re.findall(pattern, str(ob_id_tag))[0][1:-1]
            phone_hide_type = 1
            print(ob_id)

        pattern = re.compile('var phoneToken = (\'.*?\');')
        phoneToken = re.findall(pattern, str(html_l))[0][1:-1]

        if phone_hide_type == 0:
            if use_proxy == True:
                phone = requests.get("https://www.olx.ua/ajax/misc/contact/phone/{0}/?pt={1}".format(ob_id, phoneToken), headers=headers, cookies=cookies, proxies=random.choice(proxy_list)).content
            elif use_proxy == False:
                phone = requests.get("https://www.olx.ua/ajax/misc/contact/phone/{0}/?pt={1}".format(ob_id, phoneToken), headers=headers, cookies=cookies).content

            dataPhone = BeautifulSoup(phone, "lxml").find_all("span")

        elif phone_hide_type == 1:
            None
            # ?????????????????????????
            # ?????????????????????????
            # ?????????????????????????
            # ?????????????????????????

        phone_number = []

        data_json = requests.get("https://www.olx.ua/ajax/misc/contact/phone/{0}/?pt={1}".format(ob_id, phoneToken), headers=headers, cookies=cookies).json()


        if "span" in data_json["value"]:
            soup = BeautifulSoup(data_json["value"], "lxml").find_all("span")
            for text in soup:
                phone_number.append(text.text)

        else:
            phone_number.append(data_json["value"])

        phone_number.sort()
        phone_number = [el for el, _ in groupby(phone_number)]


        for i in range(len(offer_details_name_raw)):
            data[offer_details_name_raw[i].text] = offer_details_value_raw[i].text

        data["Description"] = description
        data["phone_number"] = phone_number
        data["link"] = links[link_number]

        with open("./data/links_data/link_" + str(link_number) + "_data" + '.json', 'w') as f:
            json.dump(data, f)

        time_on_one_link = time.time() - start_one_link_time
        print("ссылка:", link_number + 1, ", время на обработку ссылки:", time_on_one_link)

        # with open('./data/links.txt', 'r') as f:
        #     lines = f.readlines()
        #
        # with open('./data/links.txt', 'w') as f:
        #     f.writelines(lines[1:])

        link_number += 1

    print("потраченое время: ", int((time.time() - time_start) / 60), "min.  ", (time.time() - time_start) - int((time.time() - time_start) / 60), "sec.")
