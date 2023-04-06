import discord
import openai
import os

openai.api_key = "#OPENAI API KEY"

model_engine = "text-davinci-003"


def get_ai_answer(prompt):
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = completions.choices[0].text.strip()
    return message


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if bot's user ID is mentioned in the message content
    if client.user.mentioned_in(message):
        answer = message.content
        answer = get_ai_answer(answer)

        if len(answer) > 1999:
            answer = answer[:1999]

        # Define list of forbidden keywords
        forbidden_keywords = ["porn", "sex", "xxx", "xhamster", "pornhub"]

        # Add filter to bot's response
        if any(keyword in answer.lower() for keyword in forbidden_keywords):
            answer = "I'm sorry, I cannot send messages with 18+ content or inappropriate language."

        await message.channel.send(answer)


client.run("#Your Discord API Key")
