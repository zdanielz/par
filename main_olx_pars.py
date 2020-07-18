from olx_link_pars import BeautifulSoup
from olx_link_pars import requests
from olx_link_pars import groupby
from olx_link_pars import time
from olx_link_pars import link_parser
from olx_link_pars import random
from data import proxy_list as proxy_list_py
proxy_list = proxy_list_py.proxy_list

use_proxy = False                                                   # использовать прокси?


if proxy_list == None:
    use_proxy = False

time_start = time.time()

i = 0
i2 = 0

file = open("./input_links.txt", "r")
url = file.readlines()

for i in range(len(url) - 1):
    url[i] = url[i][0:-1]

a = []
page = 1
count_link = 0
sr_time = 0
number_main_link = 0

for i in range(len(url)):
    page = 1
    i2 = 0
    count_link = 0

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    if use_proxy == True:
        html_l = requests.get(url[number_main_link], headers=headers, proxies=random.choice(proxy_list)).content.decode("utf-8")
    elif use_proxy == False:
        html_l = requests.get(url[number_main_link], headers=headers).content.decode("utf-8")
    soup = BeautifulSoup(html_l, 'lxml').find("a", {"data-cy": "page-link-last"})

    last_page = int(soup.text)

    print(url[number_main_link])

    while i2 < last_page:
        start_one_page_time = time.time()
        if use_proxy == True:
            html = requests.get("{0}&page={1}".format(url[number_main_link], page), headers=headers, proxies=random.choice(proxy_list)).content
        elif use_proxy == False:
            html = requests.get("{0}&page={1}".format(url[number_main_link], page), headers=headers).content
        soup = BeautifulSoup(html, 'lxml')
        soup = soup.find_all("table", {"id": "offers_table"})
        link = BeautifulSoup(str(soup), 'lxml').find_all("a", {"data-cy": "listing-ad-title"})
        for href in link:
            a.append(href.get('href'))
            count_link += 1
        time_on_one_page = time.time() - start_one_page_time
        print("страница", page, ", время на обработку страницы:", time_on_one_page, "sec")
        sr_time += time_on_one_page
        page += 1
        i2 += 1

    print("ссылок:", count_link)
    number_main_link += 1

    print("#================================================================#\n")

count_link = 0
try:
    while True:
        a.remove("#")
except ValueError:
    None

a.sort()
new_a = [el for el, _ in groupby(a)]            # удаление одинаковіх ссылок
                                                # new_a - список ссылок на странице

count_link = len(new_a)

print("потраченое время: ", int((time.time() - time_start) / 60), "min.  ", (time.time() - time_start) - int((time.time() - time_start) / 60), "sec.")
print("среднее время на обработку одной страницы: ", sr_time / last_page)
print("ссылок всего: ", count_link)
print("#================================================================#\n")

f = open("./data/links.txt", "w")
for link in new_a:
    f.write("%s\n" % link)
f.close()

link_parser(proxy_list, use_proxy)

print("\n#===========================================================#\n"
      "общее потраченое время: ", int((time.time() - time_start) / 60), "min.  ", (time.time() - time_start) - int((time.time() - time_start) / 60), "sec.\n"
      "#===========================================================#\n")
