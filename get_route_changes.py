import re
import json
import requests
import time
from bs4 import BeautifulSoup
from datetime import date

user_id = '200751676/jim-howe'
user_tree = {}
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def add_route_info(route):
	route_id,route_name = re.search(r'route/(\d+)/.*><strong>(.+)</strong>',str(route)).groups()
	user_tree[route_name] = {'id':route_id}

	route_url = 'https://www.mountainproject.com/route/' + route_id + '/' + route_name
	route_response = requests.get(route_url,headers=headers)
	soup = BeautifulSoup(route_response.text,'lxml')

	# Add comment count to route info
	comment_text = soup.find("h2",{"class":"comment-count"})
	comment_count = re.search(r'>(.+) Comment',str(comment_text)).groups()[0]
	user_tree[route_name]['comments'] = comment_count	

	# Add route stats info (num ticks, ratings, etc.)
	stats_url = 'https://www.mountainproject.com/route/stats/' + route_id + '/' + route_name	
	stats_response = requests.get(stats_url,headers=headers)
	soup = BeautifulSoup(stats_response.text,'lxml')
	
	try:
		star_ratings = re.search(r'Star Ratings.*>(\d+)<',str(soup)).groups()[0]
		user_tree[route_name]['star_ratings'] = star_ratings
	except:
		user_tree[route_name]['star_ratings'] = 0


	try:
		suggested_ratings = re.search(r'Suggested Ratings.*>(\d+)<',str(soup)).groups()[0]
		user_tree[route_name]['suggested_ratings'] = suggested_ratings
	except:
		user_tree[route_name]['suggested_ratings'] = 0


	try:
		on_to_do_lists = re.search(r'On To-Do Lists.*>(\d+)<',str(soup)).groups()[0]
		user_tree[route_name]['on_to_do_lists'] = on_to_do_lists
	except:
		user_tree[route_name]['on_to_do_lists'] = 0

	
	try:
		ticks = re.search(r'Ticks.*>(\d+)<',str(soup)).groups()[0]
		user_tree[route_name]['ticks'] = ticks
	except:
		user_tree[route_name]['ticks'] = 0


def main():
	my_routes_url = 'https://www.mountainproject.com/user/' + user_id + '/routes'
	my_routes_response = requests.get(my_routes_url,headers=headers)
	soup = BeautifulSoup(my_routes_response.text,'lxml')
	route_table = soup.find("table",{"class": "table route-table hidden-xs-down"})
	route_list = [route for route in route_table.findAll('a') if 'route' in str(route)]

	# Scrape user routes, and add all info to user_tree
	for route in route_list:
		add_route_info(route)
		time.sleep(0.2)

	# Try to load old route data, if doesn't exist make one with the new data
	try:
		f = open("user_tree.json","r")
		old_user_tree = json.loads(f.read())
		f.close()
	except:
		old_user_tree = user_tree

	# Add to updates file with any new updates
	updates = 0
	f = open("updates.txt","a")
	for route in old_user_tree:
		new_stats = False
		for stat in old_user_tree[route]:
			if old_user_tree[route][stat] < user_tree[route][stat]:
				updates += 1
				new_stats = True
				stat = stat.replace('_',' ')[:-1]
				f.write('Found new ' + stat + ' for route ' + route + ' on ' + str(date.today()) + '\n')
		if new_stats:
			name = route.replace(' ','-').lower()
			route_url = 'https://www.mountainproject.com/route/' + user_tree[route]['id'] + '/' + name
			f.write(route_url + '\n\n')
	f.close()

	print('Found ' + str(updates) + ' new updates to your routes')

	# Update reference tree with newest data
	f = open("user_tree.json", "w")
	json.dump(user_tree, f)
	f.close()

if __name__ == '__main__':
	main()
