from random import randint
import time
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogFiltersRequest
from telethon.tl.types import DialogFilterDefault, DialogFilter, MessageEntityUrl, MessageEntityTextUrl
from telethon.tl.patched import MessageService
from config import API_HASH, API_ID, BACKUP,FOLDER_ID


client = TelegramClient('testing',API_ID,API_HASH)

async def main():
    folders_response = await client(GetDialogFiltersRequest())
    folders = folders_response.filters
    custom_folders = [folder for folder in folders if not isinstance(folder, DialogFilterDefault)]
    dh_folder = next((folder for folder in custom_folders if folder.id==FOLDER_ID), None)
    backup_channel=None

    async for channel in client.iter_dialogs():
        if channel.name==BACKUP:
            backup_channel= await client.get_entity(channel.id)

    for channel in dh_folder.include_peers:
        entity = await client.get_entity(channel.channel_id)
        await client.send_message(backup_channel,entity.title+":")
        if entity.broadcast:
            async for message in client.iter_messages(entity):
                if not isinstance(message, MessageService):
                    try:
                        await client.forward_messages(backup_channel, message.id, entity)
                    except errors.FloodWaitError:
                        print(f"Waiting {e.seconds} seconds to continue")
                        time.sleep(e.seconds)
                        await client.forward_messages(backup_channel, message.id, entity)
                        
        else:
            async for message in client.iter_messages(entity):
                if not isinstance(message, MessageService) and (isinstance(message,(MessageEntityUrl, MessageEntityTextUrl)) or message.media):
                    try:
                        await client.forward_messages(backup_channel, message.id, entity)
                    except errors.FloodWaitError:
                        print(f"Waiting {e.seconds} seconds to continue")
                        time.sleep(e.seconds)
                        await client.forward_messages(backup_channel, message.id, entity)

"""
async def waiting(entity="next entity"):
    wait = randint(1,15)
    print(f"Waiting {wait} seconds... to forward message from {entity.title}")
    time.sleep(wait)
"""

with client:
    client.loop.run_until_complete(main())