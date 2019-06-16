import json

from resurrectgram.crawler import Crawler


config = {}

with open('./config.json', 'r') as f:
    config = json.loads(f.read())

crawler = Crawler(config)
crawler.crawl()
crawler.destroy()
