import json
import random
from discord.ext import commands
import slack


def SxD_Bot(data): 

    Discord_Token = data['Token']['Discord']
    Slack_Token = data['Token']['Slack']

    bot = commands.Bot(command_prefix=data['Prefix'])
    slack_client = slack.WebClient(token=Slack_Token)

    @bot.listen('on_message')
    async def if_someone_mentions_me(msg):
        if msg.author == bot.user:
            return
        if bot.user.mentioned_in(msg):
            await msg.reply(random.choice(data['if_someone_mentions_me']))    

    @bot.command(name='slack', help=random.choice(data['commands']['slack']))
    async def transfer_msg(ctx, channel=None, *, msg=None):
        if msg==None:
            await ctx.reply("Usage !slack CHANNEL_NAME Message")
            return
        try:
            ch = ''.join(['#', channel])
            filtered_msg = ''.join(['{0}: '.format(ctx.author.name), msg])
            slack_client.chat_postMessage(channel=ch, text=filtered_msg)
            await ctx.reply("I've sent ur msg to {0} channel in slack!".format(channel))
        except Exception as e:
            await ctx.reply(e)

    bot.run(Discord_Token)


def main():
    file = 'data.json'
    with open(file) as f:
        data = json.load(f)
    SxD_Bot(data)


if __name__ == "__main__":
    main()