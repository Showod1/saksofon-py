import telebot
import requests

# Telegram bot token
TOKEN = '6981330258:AAF9-kLl5EcKzna7zPj9gJwedmDPzH0nW2k'

# API endpoint for aile sorgusu
AILE_API_ENDPOINT = 'https://rezidans.co/api/aile/api.php?tc='

# API endpoint for tc sorgusu
TC_API_ENDPOINT = 'https://rezidans.co/api/tc/api.php?tc='

# Bot oluştur
bot = telebot.TeleBot(TOKEN)

# Komutlar
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Benimle aşağıdaki komutları kullanabilirsiniz:\n"
                          "/aile <T.C. Kimlik No> - aile sorgusu yapar\n"
                          "/tc <T.C. Kimlik No> - tc sorgusu yapar")

@bot.message_handler(commands=['aile'])
def aile_sorgusu(message):
    # Komuttan T.C. Kimlik No'yu al
    try:
        tc_kimlik_no = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Lütfen bir T.C. Kimlik No girin.")
        return
    
    # API'ye sorgu yap
    response = requests.get(f'{AILE_API_ENDPOINT}?tc={tc_kimlik_no}')
    
    # API yanıtını kontrol et
    if response.status_code == 200:
        data = response.json()
        # Veriyi txt dosyasına yaz
        with open(f'{tc_kimlik_no}_aile.txt', 'w') as file:
            file.write(str(data))
        # Dosyayı kullanıcıya gönder
        bot.send_document(message.chat.id, open(f'{tc_kimlik_no}_aile.txt', 'rb'))
    else:
        bot.reply_to(message, "Aile bilgisi bulunamadı.")

@bot.message_handler(commands=['tc'])
def tc_sorgusu(message):
    # Komuttan T.C. Kimlik No'yu al
    try:
        tc_kimlik_no = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Lütfen bir T.C. Kimlik No girin.")
        return
    
    # API'ye sorgu yap
    response = requests.get(f'{TC_API_ENDPOINT}?tc={tc_kimlik_no}')
    
    # API yanıtını kontrol et
    if response.status_code == 200:
        data = response.json()
        # Veriyi txt dosyasına yaz
        with open(f'{tc_kimlik_no}_tc.txt', 'w') as file:
            file.write(str(data))
        # Dosyayı kullanıcıya gönder
        bot.send_document(message.chat.id, open(f'{tc_kimlik_no}_tc.txt', 'rb'))
    else:
        bot.reply_to(message, "TC bilgisi bulunamadı.")

# Bot'u çalıştır
bot.polling()
