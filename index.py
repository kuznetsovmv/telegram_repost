from telethon import TelegramClient
from telethon.events import NewMessage
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
                await client.forward_messages(channel_id, event.message)

        @client.on(NewMessage(func=filter_handle))
        async def handler(event):
            try:
                channel_id = event.to_id.channel_id
                try:
                    channel = await event.client.get_entity(channel_id)
                except ValueError:
                    return
                if channel is None:
                    print('no_channel')
                    return
                await forward(event)
            except Exception as e:
                print('ERROR: ', e, event)

        client.run_until_disconnected()


client_start()
