import json

from pymongo import MongoClient
from resurrectgram.logger import Logger
from time import sleep
from py_tdlib import Client, Pointer, Auth
from py_tdlib.constructors import getChats, getChatEventLog, getMe

class Crawler(object):
    def __init__(self, config, logger = None):
        self.data_per_page = 100
        self.config = config
        self.logger = logger

        self.client = None
        self.db = None

        self.fail_count = 0
        self.retry_count = 0
        self.current_page = 0

        if self.logger is None:
            self.logger = Logger()

    def login(self):
        self.attach_client(1)

    def chats(self):
        return self.client.send(getChats(
            offset_order=9223372036854775807,
            offset_chat_id=0,
            limit=self.config['max_chats']
        ))

    def attach_client(self, verbosity=0):
        try:
            tdjson = Pointer(self.config['tdjson_path'])
            tdjson.verbosity(verbosity)

            self.client = Client(tdjson)

            # Do you guys not have phones?
            Auth(self.config['api_id'], self.config['api_hash'], self.client).phone()

            user = self.client.send(getMe())
            self.logger.success("Successfully Authenticated as @" + user.username)

        except Exception as err:
            self.logger.error("Error while Authenticating Telegram!", err)

    def attach_database(self):
        try:
            connection = MongoClient(self.config['database_ip'], self.config['database_port'])
            self.db = connection.get_database(self.config['database_name'])

            self.logger.success("Successfully Connected Database")

        except Exception as err:
            self.logger.error("Error while Connection to Database!", err)

    def crawl_one(self, from_id = None):
        try:
            if from_id is None:
                from_id = 0

                aggregated = list(self.db.events.aggregate([
                    {"$group": {
                        "_id": None,
                        "final_crawl": { "$min": "$id" }
                    }}
                ]))

                if len(aggregated) > 0:
                    from_id = aggregated[0]['final_crawl']

                self.logger.info("Crawling from %d" % from_id)

            method = getChatEventLog(
                chat_id=self.config['chat_id'],
                from_event_id=from_id,
                limit=self.data_per_page
            )

            fetch_result = self.client.send(method)
            events = []

            for event in fetch_result.events:
                events.append(json.loads(str(event)))
                events[-1]['id'] = int(events[-1]['id'])

            self.db.events.insert_many(
                events
            )

            self.current_page += 1

            if self.retry_count > 0:
                self.fail_count -= 1
                self.retry_count = 0

            if self.fail_count > 0:
                self.logger.progress("Crawled Page #%d, Failed %d" % (self.current_page, self.fail_count))
            else:
                self.logger.progress("Crawled Page #%d" % self.current_page)

            return len(events), min([event['id'] for event in events])

        except Exception as err:
            if self.retry_count == 0:
                self.fail_count += 1
                self.logger.error("Failed fetching Page #%d" % (self.current_page + 1), err)

            else:
                self.logger.error(
                    "Failed fetching Page #%d (Retry %d)" % (self.current_page + 1, self.retry_count),
                    err
                )

            self.retry_count += 1

            return False, from_id

    def crawl(self):
        if self.config['chat_id'] not in [str(chat_id) for chat_id in self.chats().chat_ids]:
            self.logger.fatal(
                "Your chat is not in top chat lists.\n" +
                "Please increase max_chats or double check your chat_id.\n"
            )

        from_id = None

        while True:
            crawl_len, next_id = self.crawl_one(from_id)

            if (not crawl_len == False) and crawl_len < self.data_per_page:
                self.logger.complete(
                    "Completed crawling (Crawled %d, Failed %d)" % (
                        self.current_page * self.data_per_page, self.fail_count
                    )
                )

                break

            elif crawl_len == False and self.retry_count > self.config['max_retry']:
                self.logger.complete(
                    "Completed crawling w/ Failure at Event %s, (Crawled %d, Failed %d)" % (
                        from_id, self.current_page * self.data_per_page, self.fail_count
                    )
                )

                break

            from_id = next_id

            sleep(self.config['send_rate'])

    def destroy(self):
        self.client.stop()
