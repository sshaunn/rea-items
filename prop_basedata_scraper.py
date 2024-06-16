import csv
import json
import logging
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Create the ChromeDriver service
service = Service('~/Git/chromedriver/')
options = webdriver.ChromeOptions().add_argument('--incognito')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

links = []
with open("property_links.txt", 'r') as links_list:
    lines = links_list.readlines()

    for line in lines:
        links.append(line)

for link in links:
    print(f"opt link = %s", link)
    driver.get(link)
    html = driver.page_source

    parts = html.split("var digitalData = ")

    if len(parts) > 1:
        digital_data_part = parts[1]

        data_layer_part = digital_data_part.split("var dataLayer = ")
        if len(data_layer_part) > 1:
            result = data_layer_part[0].rstrip()[:-1]
            print(f"current prop data = %s", result)
            data: dict = json.loads(result)
            print(f"current prop data = %s", data)
            prop_data = {}
            headers = ["address",
                       "bathrooms",
                       "bedrooms",
                       "parking",
                       "landArea",
                       "price",
                       "primaryPropertyType",
                       "propertyFeatures",
                       "state",
                       "suburb",
                       "postcode"]

            prop_data["address"] = data["page"]["pageInfo"]["property"].get("address", "")
            prop_data["bathrooms"] = data["page"]["pageInfo"]["property"].get("bathrooms", "")
            prop_data["bedrooms"] = data["page"]["pageInfo"]["property"].get("bedrooms", "")
            prop_data["parking"] = data["page"]["pageInfo"]["property"].get("parking", "")
            prop_data["landArea"] = data["page"]["pageInfo"]["property"].get("landArea", "")
            prop_data["price"] = data["page"]["pageInfo"]["property"].get("price", "")
            prop_data["primaryPropertyType"] = data["page"]["pageInfo"]["property"].get("primaryPropertyType", "")
            prop_data["propertyFeatures"] = data["page"]["pageInfo"]["property"].get("propertyFeatures", "")
            prop_data["state"] = data["page"]["pageInfo"]["property"].get("state", "")
            prop_data["suburb"] = data["page"]["pageInfo"]["property"].get("suburb", "")
            prop_data["postcode"] = data["page"]["pageInfo"]["property"].get("postcode", "")

            with open("prop_base_data.csv", 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                if csvfile.tell() == 0:
                    writer.writeheader()

                writer.writerow(prop_data)
            time.sleep(3)

driver.quit()
