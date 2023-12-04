from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.types import PeerChannel
import json

SESSION_NAME = 'telegram_re_poster'


def client_start():
    with open('config.json') as config_file:
        config = json.load(config_file)
    with TelegramClient(
            session=SESSION_NAME,
            api_hash=config['api_hash'],
            api_id=config['api_id']).start(phone=config['client_phone']) as client:
        print('Telegram connected')

        def filter_handle(event):
            try:
                return event.to_id.channel_id not in config['recipient_channel_ids']
            except:
                return False

        async def forward(event):
            for channel_id in config['recipient_channel_ids']:
                try:
                    channel = await client.get_entity(PeerChannel(-abs(channel_id)))
                except Exception as e:
                    print('ERROR: recipient channel not found', e)
                    return
                await client.forward_messages(channel, messages=event.message)

        @client.on(NewMessage(func=filter_handle))
        async def handler(event):
            try:
                await forward(event)
            except Exception as e:
                print('ERROR: ', e, event)

        client.run_until_disconnected()


client_start()
