from telethon import TelegramClient, events
from PIL import Image, ImageDraw, ImageFont
import os
import time
import emoji  # Biblioteca pentru a trata emoji-urile

# Datele de autentificare pentru Telegram
api_id = '21637202'
api_hash = 'e467998da44af30e7e9485221a50cc3b'
phone_number = '+40787689817'

# ID-ul grupului de unde monitorizezi mesajele și ID-ul grupului unde trimiți screenshot-urile
source_chat_id = -4554333354  # ID-ul grupului sursă
target_chat_id = -4554333354  # ID-ul grupului destinație

# Creează clientul pentru Telegram, folosind contul personal
client = TelegramClient('session_name', api_id, api_hash)

# Autentificare și obținerea entităților
async def main():
    await client.start(phone=phone_number)  # Autentifică-te folosind contul tău

    # Obține entitățile pentru grupurile sursă și destinație
    source_chat = await client.get_input_entity(source_chat_id)
    target_chat = await client.get_input_entity(target_chat_id)

    @client.on(events.NewMessage(chats=source_chat))
    async def handler(event):
        # Obține mesajul
        message = event.message
        print(f"Mesaj nou: {message}")

        # Verifică dacă mesajul conține media (poză)
        if message.media and hasattr(message.media, 'photo'):
            # Descarcă poza la dimensiunea originală
            file_path = await client.download_media(message.media)
            
            # Extrage prima linie din mesaj
            first_line = message.message.split('\n')[0] if message.message else 'Poză trimisă'

            # Trimite poza la dimensiunea originală cu prima linie ca descriere
            await client.send_file(target_chat, file_path, caption=first_line)
            
            # Șterge poza după trimitere pentru a elibera spațiu
            os.remove(file_path)
        
        # Dacă mesajul conține text, creează o imagine cu textul și emoji-urile
        elif message.message:
            # Extrage textul mesajului, inclusiv emoji-urile
            message_text = message.message
            
            # Setează fontul
            try:
                font = ImageFont.truetype("arial.ttf", 20)  # Font standard
            except IOError:
                font = ImageFont.load_default()  # În caz că fontul nu e găsit, folosește unul implicit

            # Creează o imagine temporară pentru a calcula dimensiunea textului
            temp_image = Image.new('RGB', (1, 1))
            draw = ImageDraw.Draw(temp_image)

            # Calculează dimensiunea necesară pentru text
            bbox = draw.textbbox((0, 0), emoji.emojize(message_text), font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            padding = 20  # Adaugă un mic spațiu de margine în jurul textului

            # Creează imaginea finală cu dimensiunea exactă pentru text
            image = Image.new('RGB', (text_width + padding, text_height + padding), color=(255, 255, 255))
            draw = ImageDraw.Draw(image)

            # Adaugă textul mesajului în imagine, incluzând emoji-urile
            draw.text((padding // 2, padding // 2), emoji.emojize(message_text), fill=(0, 0, 0), font=font)

            # Salvează imaginea creată
            screenshot_path = f"screenshot_{int(time.time())}.png"
            image.save(screenshot_path)

            # Extrage prima linie din mesaj pentru caption
            first_line = message_text.split('\n')[0]

            # Trimite imaginea în grupul țintă cu prima linie ca descriere
            await client.send_file(target_chat, screenshot_path, caption=first_line)

            # Șterge imaginea după trimitere
            os.remove(screenshot_path)

    print("Monitorizez mesajele...")
    await client.run_until_disconnected()

# Pornește clientul și rulează funcția
with client:
    client.loop.run_until_complete(main())