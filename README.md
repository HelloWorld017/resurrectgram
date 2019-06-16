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
5. Create configuration: `config.js`  
6. Create directory `data/sessions/default`  
7. `python3 main.py login`  
8. `python3 main.py`

### Example configuration
```js
{
	"api_id": 1234567,
	"api_hash": "0123456789abcdef0123456789abcdef",
	"chat_id": "-1234567890123", // Your group id
	"send_rate": 1, // req/sec
	"max_retry": 5,
	"tdjson_path": "lib/tdjson.dll", // Path to tdjson.dll

	"database_ip": "127.0.0.1", // MongoDB ip
	"database_port": 27017, // MongoDB port
	"database_name": "resurrectgram" // MongoDB Database Name
}
```

You can get api_id and api_hash from [here](https://my.telegram.org/apps)
