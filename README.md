# Telegram auto-forwarding

## Installation

```bash
pip3 install -r requirements.txt
```

## Configuration

Add `config.json` file that looks like this

```json
{
    "api_id": 123,
    "api_hash": "my_hash_value",
    "client_phone": "+123123123",
    "recipient_channel_ids": []
}
```

`api_id` - Telegram api_id  
`api_hash` - Telegram api_hash  
`client_phone` - phone number to log in  
`recipient_channel_ids` - list of channel ids to forward your posts to 

More about Telegram api_id and api_hash read [here](https://core.telegram.org/api/obtaining_api_id)

## Run

Start like this

```bash
python3 index.py
```

Or with run parameters

```bash
python3 index.py --session=telegram_session --config=config.json
```

### Run parameters

| Name      | Description                   | Required | Default Value    |
|-----------|-------------------------------|----------|------------------|
| `session` | name of your Telegram session | No       | telegram_forward |
| `config`  | config file name              | No       | config.json      |

you can find yor run log at `<session_name>.log` file (`telegram_forward.log` by default)