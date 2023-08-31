import discord
import responses
from datetime import datetime

async def send_message(message, user_message, is_private):
	try:
		response = responses.get_response(message)

		# Check that response is not empty before sending
		if response and (response.message or response.file):
			target = message.author if is_private else message.channel

			if response.file:
				await target.send(content = response.message, file = response.file)
			else:
				await target.send(response.message)

	except Exception as e:
		print(e)

async def send(message):
	await message.channel.send('No-one asked for your opinion donbass')

def get_time():
	dt = datetime.now()
	t = f'{dt.year}-{dt.month}-{dt.day} {dt.hour}:{dt.minute}:{dt.second}'
	return t

def run_bot():
	with open("token.txt") as f:
		TOKEN = f.readline()
		print(TOKEN)
	intents = discord.Intents.default()
	intents.message_content = True
	global client
	client = discord.Client(intents = intents)

	@client.event
	async def on_ready():
		print(f'{get_time()} - {client.user} is running')

	@client.event
	async def on_message(message):
		if message.author == client.user:
			return

		username = str(message.author.name)
		user_message = str(message.content)
		channel = str(message.channel)

		print(f'{get_time()} - {username} said "{user_message}" ({channel})')

		if user_message[0] == '_':
			user_message = user_message[1:]
			await send_message(message, user_message, is_private = True)
		else:
			await send_message(message, user_message, is_private = False)

	client.run(TOKEN)
