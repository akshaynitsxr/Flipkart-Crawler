from urllib2 import Request, urlopen
from pprint import pprint
from bs4 import BeautifulSoup, Comment
from urlparse import urlparse, parse_qs
import json
import requests
import BeautifulSoup
import pdb
import json
import redis
import time

def findItem(link,file):
    flag = 0
    headers = {"content-type": "application/json"}
    parameters = {"requestContext":{"store": "search.flipkart.com", "start": 0, "disableProductData": "true", "count": "100", "q": "moto%20g", "ssid": "j2dh05ke000000001505984994890", "sqid": "8ip4gpojxc0000001505984994890"}}
    try:
    	r = requests.post(link, data = parameters)
    except Exception, e:
    	time.sleep(3)
    	try:
    		r = requests.post(link, data = parameters)
    	except Exception, e:
    		flag = 1
    if flag==0:
	    data = r.text.encode('UTF-8')
	    soup = BeautifulSoup.BeautifulSoup(data)
	    
	    prod = soup.findAll('a', {'class' : '_2cLu-l'})
	    prices = soup.findAll('div',{'class' : '_1vC4OE'})
	    mrp_prices = soup.findAll('div',{'class' : '_3auQ3N'})
	    product = []
	    x = [int(str(v).split('-->')[-2].split('<!--')[0].replace(',','')) for v in prices]
	    for i, value in enumerate(prod):
	        o= urlparse(value['href'])
	        temp = {}
	        temp['title'] = value['title']
	        temp['pid'] = parse_qs(o.query)['pid'][0]
	        try:
	        	temp['price'] = int(str(prices[i]).split('-->')[-2].split('<!--')[0].replace(',',''))
	    	except Exception, e:
	    		temp['price'] = 0
	        try:
	            temp['mrp_price'] = int(str(mrp_prices[i]).split('-->')[-2].split('<!--')[0].replace(',',''))
	        except Exception, e:
	            temp['mrp_price'] = 0
	        
	        product.append(temp)
	        file.write(str(temp))
	    # print product

	    print len(prod)
	    # reuest_body = response.read()
	    # data = json.load(response);
	    return


def crawl():
    
    link = "https://www.flipkart.com/lc/getData?dataSourceId=websiteNavigationMenuDS_1.0"
    r = requests.get(link)
    data = json.loads(r.text.encode('UTF-8'));
    # pprint(data)
    file = open("MRPFile5.txt","w")
    for value in data['navData']:
        if data['navData'][value]['url'] == '#':
	        for j in range(len(data['navData'][value]["tabs"][0]["columns"])):
	            for i in range(len(data['navData'][value]["tabs"][0]["columns"][j])):
	                findItem("https://www.flipkart.com" + data['navData'][value]["tabs"][0]["columns"][j][i]["url"],file);
        # for i in len(value['tabs'][0].columns[0]):
        #     print value['tabs'][0].columns[0][i]

    file.close()
    return

crawl()
# findItem("moto g")
# findItem("Giordano Analog Watch")
# findItem("nosuchitemfound")