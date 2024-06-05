import telebot
import os

# Replace 'YOUR_BOT_TOKEN' with your bot's token
API_TOKEN = '7407329965:AAE9jZg86O4UTbvLJGDrX-Ehl3W63B6x2Xc'
# Replace 'YOUR_CHANNEL_ID' with your channel's ID (e.g., '@your_channel')
CHANNEL_ID = '@anon_caption_remover_bot'

bot = telebot.TeleBot(API_TOKEN)

# Function to handle media messages
def handle_media(message):
    file_id = None

    if message.photo:
        file_id = message.photo[-1].file_id  # Get the highest resolution photo
    elif message.video:
        file_id = message.video.file_id
    elif message.document:
        file_id = message.document.file_id

    if file_id:
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = file_info.file_path.split('/')[-1]

        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)

        with open(file_name, 'rb') as new_file:
            if message.photo:
                bot.send_photo(CHANNEL_ID, new_file)
            elif message.video:
                bot.send_video(CHANNEL_ID, new_file)
            elif message.document:
                bot.send_document(CHANNEL_ID, new_file)

        os.remove(file_name)

@bot.message_handler(content_types=['photo', 'video', 'document'])
def media_message_handler(message):
    if message.caption:
        handle_media(message)
    else:
        if message.photo:
            bot.send_photo(CHANNEL_ID, message.photo[-1].file_id)
        elif message.video:
            bot.send_video(CHANNEL_ID, message.video.file_id)
        elif message.document:
            bot.send_document(CHANNEL_ID, message.document.file_id)

# Start polling
bot.polling(none_stop=True)
