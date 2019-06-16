import json
import sys

from resurrectgram.crawler import Crawler


config = {}

with open('./config.json', 'r') as f:
    config = json.loads(f.read())

crawler = Crawler(config)

if len(sys.argv) > 1 and sys.argv[1] == 'login':
    crawler.login()

else:
    crawler.attach_database()
    crawler.attach_client()
    crawler.crawl()

crawler.destroy()
