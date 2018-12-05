
# coding: utf-8

# In[8]:


import bs4 as bs
import urllib.request
from time import localtime, strftime
import csv

price_IDS = [{"id": "priceblock_ourprice"},
             {"id": "priceblock_dealprice"},
             {"class": "a-size-medium a-color-price offer-price a-text-normal"},
            {"class": "a-size-base a-color-price offer-price a-text-normal"},
            {"id": "newBuyBoxPrice"},
            {"class": "a-size-mini twisterSwatchPrice"}]

def main():
    
    items = uniqueItems()
    passList = []
    
    for item in items:
        with open('AmazonItemsTest.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                if item == row[0]:
                    passList.append(scrape_info(row[3]))
    fileAdd(passList)
        
        
        
        
#Scrapping Function; copied exactly from the main program
def scrape_info(url):
    user_agent = "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
    headers = {'User-Agent': user_agent}
    data = None
    req = urllib.request.Request(url, data, headers)
    sauce = urllib.request.urlopen(req).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    
    #Find the price on the Amazon page by checking for different tags that may contain the price
    #This function will loop through all known identifiers until it finds a price or runs out of identifiers to try
    for identifier in price_IDS:
        #Pass an identifier to the .find() function
        price_tag = soup.find("span", identifier)
        #If that identifier returned something, stop looking
        if price_tag != None:
            break
    
    #This block of code is in case there is no price on the page or the Amazon page is weird and the price is in a tag not known to us

    try:
        price = price_tag.text
    except:
        price = "Sorry, there is no available price for this item at this time"

    #Find the item name on the Amazon page
    itemName = soup.find("span", {"id": "productTitle"})
    
    amazonItem = {'Item': itemName.text.strip(), 'Price': price, 'Time': strftime("%Y-%m-%d %H:%M:%S", localtime()), 'URL': url}
    #amazonItem = { itemName.text.strip() : [price, strftime("%Y-%m-%d %H:%M:%S", localtime())]}
    return amazonItem

#Appending item entries to the list of tracked items
def fileAdd(newItems):
    with open('AmazonItemsTest.csv', 'a', newline='') as itemsFile: #11/8/18 using 'AmazonItemsTest.csv' for testing purposes
        fieldnames = ['Item', 'Price', 'Time', 'URL']
        theWriter = csv.DictWriter(itemsFile, fieldnames=fieldnames)
        
        for item in newItems:
            theWriter.writerow(item)
    print('Success')
            
def uniqueItems():
    unique_items = []

    #to fill unique items list
    with open("AmazonItemsTest.csv", "r") as csvFile:
        readCSV = csv.reader(csvFile, delimiter=',')
        for row in readCSV:
            if row[0] not in unique_items:
                unique_items.append(row[0])


    #to correct the the unique items list 
    unique_items.pop(0)
    #print(unique_items)
    return unique_items
            
main()

