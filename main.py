import discord
import openai
import os

TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)

openai.api_key = OPENAI_KEY

@client.event
async def on_ready():
    print(f'Bot is ready. Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!ask"):
        prompt = message.content[5:]
        await message.channel.send("🤖 Thinking...")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response['choices'][0]['message']['content']
            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send(f"❌ Error: {str(e)}")

client.run(TOKEN)
