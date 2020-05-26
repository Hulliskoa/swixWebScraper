from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import json
from selenium.webdriver.chrome.service import Service


service = Service('./chromedriver')
service.start()
kotlinFile = open('kotlinProducts.json', 'w')
jsondata = {}
productList = []
op = webdriver.ChromeOptions()
op.add_argument('headless')


def scrapeSwix(categoryParam, genderType):
	driver = webdriver.Chrome(options=op)
	driver.get("https://www.swixsport.com/no/klar/" + genderType + "/" + categoryParam + "/")
	links = []
	containers = driver.find_elements_by_class_name('product-card__link')
	visitedLinks = []

	for link in containers:
		links.append(link.get_attribute("href"))


	for link in links:

		if link in visitedLinks:
			continue

	
		driver.get(link)
		
		productData = {}
		colorImages = []

		productData ['name'] = driver.find_element_by_xpath('/html/body/main/section/div[1]/div/section/div/div/div[1]/h1/span').get_attribute("innerHTML").encode("utf-8") 
		productData ['category'] = categoryParam.encode("utf-8")
		
		productData ['description'] = driver.find_element_by_xpath('/html/body/main/section/div[1]/div/section/div/div/div[3]/div/p[1]').get_attribute("innerHTML").encode("utf-8")
		productData ['gender'] = genderType.encode("utf-8")
		
		productData ['subCategory'] = 'na'
		productData ['brand'] = 'swix'

		colorContainers = driver.find_elements_by_class_name('variants__variant-color')
		variantId = []

		for textId in colorContainers:
			variantId.append(textId.get_attribute("id"))

		for variant in variantId:
			driver.get(driver.find_element_by_xpath('//*[@id="html"]/head/meta[7]').get_attribute('content') + '?code=' + variant)
			
			colorImage = {}
			colorImage["color"] = driver.find_element_by_xpath('/html/body/main/section/div[1]/div/section/section/div/section[2]/div/div/section/article[2]/ul/li[1]/span[2]').get_attribute("innerHTML").encode("utf-8")
			colorImage["image"] = driver.find_element_by_xpath('/html/body/main/section/div[1]/div/section/div/div/div[2]/div/div[1]/div[1]/div[1]/img').get_attribute("src")
	
			colorImages.append(colorImage)
			visitedLinks.append('https://www.swixsport.com/no/klar/herre/jakker/blizzard-anorak-m/?code=' + variant)


		sizes = driver.find_elements_by_class_name("variants__variant-size")
		textSizes = []
		for size in sizes:
			#if size.get_attribute("class") == "variants__variant-size variants__variant-size--disabled":
				#continue
			textSizes.append(size.find_element_by_class_name("variants__variant-size__text").get_attribute("innerHTML"))

		productData["sizes"] = textSizes 
		productData ['colorImages'] = colorImages
		productList.append(productData)
		


scrapeSwix('jakker', 'herre')
#test('jakker', 'herre')


jsondata['productCollection'] = productList
kotlinFile.write(json.dumps(jsondata))

print(json.dumps(jsondata))

