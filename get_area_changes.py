import requests
from bs4 import BeautifulSoup
import time
import smtplib

area_id = '108811240'

def main():
	area_url = 'https://www.mountainproject.com/area/' + area_id
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	response = requests.get(area_url,headers=headers)
	soup = BeautifulSoup(response.text, 'lxml')
	route_list = soup.find("table", {"id": "left-nav-route-table"}).findAll('a')
	print(route_list)

if __name__ == '__main__':
	main()
