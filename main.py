import requests
import json
import telebot

# Chave do bot no Telegram
bot_key = 'BOT KEY AQUI'

# Chave da API da OpenAI
openai_key = 'OPENAI KEY AQUI'

# URL da API
api_url = 'https://api.openai.com/v1/chat/completions'

# Função para enviar mensagem para a API
def send_message(messages, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_key}'
    }

    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages + [{"role": "user", "content": message}]
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return json.loads(response.text)['choices'][0]['message']['content']
    else:
        return None

# Inicializa o bot
bot = telebot.TeleBot(bot_key)

# Armazena as mensagens da conversa
conversation = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Olá! Eu sou o ChatPEO. Me envie uma mensagem e eu tentarei respondê-lo da melhor forma possível.")

# Função para responder as mensagens
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Adiciona a mensagem atual à lista
    conversation.append({"role": "user", "content": message.text})

    # Envia a mensagem para a API
    response = send_message(conversation, message.text)

    if response is not None:
        # Adiciona a mensagem da API à lista
        conversation.append({"role": "assistant", "content": response})

        # Envia a resposta do bot
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, 'Desculpe, não consegui entender.')

# Inicia o bot
bot.polling()
