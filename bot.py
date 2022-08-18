import discord
from discord import utils

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

import config

intents = discord.Intents.all()
intents.members = True

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id) # getting the channel object
            message = await channel.fetch_message(payload.message_id) # getting the message object
            member = utils.get(message.guild.members, id=payload.user_id) # we get the object of the user who set the reaction

            try:
                emoji = str(payload.emoji) # the emoji that the user chose
                role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # объект выбранной роли (если есть)

                if(len([i for i in member.roles if i.id not in config.EXCROLES]) <= config.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))

            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)

            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) # getting the channel object
        message = await channel.fetch_message(payload.message_id) # getting the message object
        member = utils.get(message.guild.members, id=payload.user_id) # we get the object of the user who set the reaction

        try:
            emoji = str(payload.emoji) # the emoji that the user chose
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # the object of the selected role (if any)

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


client = discord.Client(intents=intents)
client = MyClient(intents = discord.Intents.all())
# RUN
client.run(config.TOKEN)
