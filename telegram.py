from telethon import TelegramClient, events
import re
import requests

# Substitua pelos seus próprios valores
api_id = '24987097'
api_hash = 'e0cd251ed34271ccbf69dc20324231fc'
phone_number = '+5511949443193'

# ID do canal
channel_id = -1001707440698

# Credenciais do CallMeBot
callmebot_phone = '+5511949443193'  # Seu número de WhatsApp, incluindo o código do país
callmebot_api_key = '5789706'

# Cria o cliente do Telegram
client = TelegramClient('session_name', api_id, api_hash)

# Expressão regular para encontrar a porcentagem na mensagem
pattern = re.compile(r"OVER 0\.5 HT: (\d+\.\d+)%")

# Define o handler para novas mensagens
@client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    print(f"Nova mensagem recebida: {event.message.message}")
    match = pattern.search(event.message.message)
    if match:
        percentage = float(match.group(1))
        if percentage >= 75.0:
            print(f"Mensagem atende aos critérios: {event.message.message}")
            # Envia a mensagem via CallMeBot
            send_whatsapp_message(event.message.message)
        else:
            print(f"Mensagem não atende aos critérios: {percentage}%")
    else:
        print("Mensagem não contém a porcentagem desejada.")

def send_whatsapp_message(message):
    url = f'https://api.callmebot.com/whatsapp.php?phone={callmebot_phone}&text={message}&apikey={callmebot_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        print('Mensagem enviada com sucesso!')
    else:
        print(f'Falha ao enviar mensagem. Status code: {response.status_code}, Response: {response.text}')

async def main():
    await client.start(phone_number)
    print("Cliente iniciado")
    # Executa o cliente e mantém o loop rodando
    await client.run_until_disconnected()

# Executa o cliente
with client:
    client.loop.run_until_complete(main())