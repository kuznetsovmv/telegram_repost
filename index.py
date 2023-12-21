import sys
from telethon import TelegramClient
from telethon.events import NewMessage
from telethon.tl.types import PeerChannel
import logging
import json
import argparse

DEFAULT_SESSION_NAME = 'telegram_forward'
DEFAULT_CONFIG_FILE_NAME = 'config.json'


def client_start(session_name=DEFAULT_SESSION_NAME, config_file_name=DEFAULT_CONFIG_FILE_NAME, log_to_file=False):
    log_format = '%(asctime)s %(levelname)s %(message)s'
    log_level = logging.INFO
    if log_to_file:
        logging.basicConfig(
            level=log_level,
            filename=f'{session_name}.log',
            format=log_format
        )
    else:
        logging.basicConfig(
            stream=sys.stdout,
            level=log_level,
            format=log_format
        )
    logger = logging.getLogger()

    with open(config_file_name) as config_file:
        config = json.load(config_file)

    with TelegramClient(
            session=session_name,
            api_hash=config['api_hash'],
            api_id=config['api_id'],
            system_version=config['system_version']
    ).start(phone=config['client_phone']) as client:
        logger.info('Telegram connected')

        def filter_handle(event):
            try:
                return event.to_id.channel_id not in config['recipient_channel_ids']
            except Exception as e:
                logger.error('filter exception', exc_info=e)
                return False

        async def forward(event):
            for channel_id in config['recipient_channel_ids']:
                try:
                    channel = await client.get_entity(PeerChannel(-abs(channel_id)))
                except Exception as e:
                    logger.error('recipient channel not found', exc_info=e)
                    return
                await client.forward_messages(channel, messages=event.message)

        @client.on(NewMessage(func=filter_handle))
        async def handler(event):
            try:
                await forward(event)
            except Exception as e:
                logger.error('forwarding error', exc_info=e)

        client.run_until_disconnected()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Settings for')
    parser.add_argument("--session", type=str, default=DEFAULT_SESSION_NAME, required=False)
    parser.add_argument("--config", type=str, default=DEFAULT_CONFIG_FILE_NAME, required=False)
    parser.add_argument("--log_to_file", choices=[0, 1], type=int, default=0, required=False)
    args = parser.parse_args()
    client_start(session_name=args.session, config_file_name=args.config, log_to_file=args.log_to_file)
