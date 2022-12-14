import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# http://myhttpheader.com/
# get to the above website and get your header parmeters like User-Agent and Accept-Language (important)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

r = requests.get(
    "https://www.zillow.com/homes/San-Francisco,-CA_rb/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D",
    headers=headers)

data = r.text

soup = BeautifulSoup(data, "html.parser")

all_link_elements = soup.select(".KzAaq a")

all_links = []
for link in all_link_elements:
    href = link["href"]
    if "http" not in href:
        all_links.append(f"https://www.zillow.com{href}")
    else:
        all_links.append(href)

# print(all_links)
# print(len(all_links))

prices = soup.select(".kJFQQX span")
all_prices = []

for i in prices:
    if "+" in i:
        all_prices.append(i.text.split("+")[0])
    else:
        all_prices.append(i.text.split("/")[0])

all_prices = [i.split("+")[0] for i in all_prices]

# print(all_prices)
# print(len(all_prices))

discription = soup.select(selector=".property-card-link")

all_address = [i.text for i in discription if i.text != ""]

# print(all_address)
# print(len(all_address))

list1 = []

for i in range(len(all_prices)):

    print(f"Link : {all_links[i]}")
    print(f"Price : {all_prices[i]}")
    print(f"address : {all_address[i]}\n")

    dict = {
        "date and Time": datetime.datetime.now(),
        "Link": all_links[i],
        "Price": all_prices[i],
        "address": all_address[i]
    }
    list1.append(dict)


df = pd.DataFrame(list1)

df.to_excel("file.xlsx")
# or
df.to_csv("file.csv")
