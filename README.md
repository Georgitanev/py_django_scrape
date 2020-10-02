#To run the scraper: go to directory with: cd scraper

#and run with: scrapy crawl posts

# to run django REST API:
cd MyApi
python manage.py runserver

Every run it make 100-140 records because there is limit of records. 
65 sec / reccord
Run it 2-5 times intil stop crawling urls.
If all url's are crawled it stop downloaing.

And captcha reaction afrer the limit.
And sometimes website not working.


Spyder code: https://github.com/Georgitanev/py_django_scrape/blob/main/scraper/scraper/spiders/profiles.py

db.sqlite https://github.com/Georgitanev/py_django_scrape/blob/main/MyApi/db.sqlite3

Db path in 'py\scraper\scraper.py':17 row
to change db path 'D:\\git\\24_09_2019_download_repos\\py\\MyApi\\db.sqlite3'
DB.table = 'Parliament1'

http://127.0.0.1:8000/scraping-app/mp:?id=30
added:
HTTP 200 OK
Allow: GET, OPTIONS
Content-Type: application/json
Vary: Accept
