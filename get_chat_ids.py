from telethon import TelegramClient

# Înlocuiește cu datele tale
api_id = '21637202'
api_hash = 'e467998da44af30e7e9485221a50cc3b'
phone_number = '+40787689817'

# Creează clientul pentru Telegram
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # Autentifică-te
    await client.start(phone=phone_number)

    # Listează toate dialogurile (conversațiile)
    async for dialog in client.iter_dialogs():
        print(f"{dialog.name}: {dialog.id}")

# Pornește clientul și rulează funcția
with client:
    client.loop.run_until_complete(main())
