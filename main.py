import json
import sys

from resurrectgram.crawler import Crawler


config = {}

with open('./config.json', 'r') as f:
    config = json.loads(f.read())

crawler = Crawler(config)

if len(sys.argv) > 1 and sys.argv[1] == 'login':
    crawler.login()

elif len(sys.argv) > 1 and sys.argv[1] == 'chats':
    crawler.attach_client()
    chat_list = crawler.chats().chat_ids
    print()
    print("List of your chat IDs from top")
    print("====================================")
    print(", ".join([str(chat_id) for chat_id in chat_list]))

else:
    crawler.attach_database()
    crawler.attach_client()
    crawler.crawl()

crawler.destroy()
