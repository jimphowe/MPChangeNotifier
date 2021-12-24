# MPChangeNotifier

This script lets you know about any changes to routes you have uploaded to mountain project.

Changes include:
  - New Comments
  - New Star Ratings
  - New On To-Do Lists
  - New Ticks
  - New Suggested Ratings
  
  To use it, download the 'get_route_changes.py' file, and modify your user-id string on line 8 (find this in the url when you log in to MP)
  
  When you run it for the first time, it will write the file user_tree.json. This stores a copy of your current routes and their stats.
  
  When you run it in the future, new data will be compared against this file, and any changes will be written to the updates.txt file, before
  the user_tree.json file is updated to match the newest data.
