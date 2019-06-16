# Resurrectgram
Resurrect your deleted Telegram chats in group with admin rights!

## Description
This is a tool to export Recent Activity in admin menu of telegram group chats.

## Installation
1. Clone resurrectgram  
`$ git clone https://github.com/HelloWorld017/resurrectgram`  
2. Install libraries using requirements.txt
`$ pip3 install -r requirements.txt`  
`$ pip3 install git+https://github.com/andrew-ld/python-tdlib` (The author didn't uploaded it to PyPI)  
3. Build tdjson library (you can find informations about builds [here](https://tdlib.github.io/td/build.html))
and place it in resurrectgram directory  
4. Install mongodb  
5. Create configuration: `config.json`  
6. Create directory `data/sessions/default`  
7. `python3 main.py login`  
8. `python3 main.py chats`  
9. `python3 main.py`

### Example configuration
```js
{
	"api_id": 1234567,
	"api_hash": "0123456789abcdef0123456789abcdef",
	"chat_id": "-1234567890123",
	"send_rate": 1,
	"max_chats": 200,
	"max_retry": 5,
	"tdjson_path": "lib/tdjson.dll",

	"database_ip": "127.0.0.1",
	"database_port": 27017,
	"database_name": "resurrectgram"
}
```

**Explanation**

* api_id, api_hash:
You can get api_id and api_hash from [here](https://my.telegram.org/apps)  
* chat_id:
Your group id. You can get it by `python3 main.py chats` but it only returns bunch of chat IDs.  
Please use another way to get chat ID  
* send_rate: request per seconds  
* max_chats: Amount of chat lists to load.  
If you're group is not in top N chat lists (N: max_chats), the crawling process might have errors.  
* max_retry: Maximum amount to retry if fetching recent log fails.  
* tdjson_path: Path to tdjson.dll  
* database_ip, database_port, database_name: IP, Port, DB Name of your MongoDB
