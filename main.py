import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import ButtonStyle
from keep_alive import keep_alive
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
import datetime
import yt_dlp
import random

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def форум(ctx):
    embed = discord.Embed(
        title="📌 Разделы форума проекта Ordium",
        description="Выберите нужный раздел ниже с помощью кнопок ⬇️",
        color=discord.Color.blurple()
    )
    embed.set_image(url="https://media.discordapp.net/attachments/1115558412252626944/1388975058407522377/6ce019d4dd5edc78.png?ex=6862ef53&is=68619dd3&hm=c9b9f0c44fc7d121e61d92d5e64bf3cf5dce73e125395b97f2388d111f74293a&=&format=webp&quality=lossless")
    embed.set_footer(text="Проект Ordium • Форум-система")

    view = View()
    view.add_item(Button(label="🔍 Поиск напарников", style=ButtonStyle.link, url="https://discord.com/channels/1389496320846463067/1389507049544618065"))
    view.add_item(Button(label="🟩 Minecraft-контент", style=ButtonStyle.link, url="https://discord.com/channels/1389496320846463067/1389510596843667617"))

    await ctx.send(embed=embed, view=view)

# ... (весь оставшийся код не влезает в один блок, продолжим после)

class MenuView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="📖 Правила", style=discord.ButtonStyle.secondary, custom_id="rules"))
        self.add_item(Button(label="💬 Q&A", style=discord.ButtonStyle.secondary, custom_id="qa"))
        self.add_item(Button(label="ℹ Инфо", style=discord.ButtonStyle.secondary, custom_id="info"))
        self.add_item(Button(label="🎫 Тикет", style=discord.ButtonStyle.danger, custom_id="ticket"))

@bot.event
async def on_ready():
    print(f"✅ Бот запущен как {bot.user}")

@bot.command()
async def тест(ctx):
    await ctx.send(f"✅ Привет, {ctx.author.mention}! Бот Ordium на связи.")

@bot.command()
@commands.has_role("Лорд")
async def меню(ctx):
    embed = discord.Embed(
        title="📋 Главное меню",
        description="Выбери интересующий раздел ниже:",
        color=0x2f3136
    )
    embed.set_image(url="https://media.discordapp.net/attachments/1115558412252626944/1388975058407522377/6ce019d4dd5edc78.png?ex=6862ef53&is=68619dd3&hm=c9b9f0c44fc7d121e61d92d5e64bf3cf5dce73e125395b97f2388d111f74293a&=&format=webp&quality=lossless")
    await ctx.send(embed=embed, view=MenuView())

# ... код обрезан, добавим остальной код в следующем блоке

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        cid = interaction.data.get("custom_id")

        if cid == "rules":
            embed = discord.Embed(
                title="📖 Правила сервера Ordium",
                description="Пожалуйста, ознакомьтесь с основными и дополнительными правилами проекта.",
                color=0x5865F2
            )
            embed.add_field(name="📜 Базовые принципы:", value="...", inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif cid == "qa":
            embed = discord.Embed(title="💬 Часто задаваемые вопросы (Q&A)", description="...", color=0x00b894)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif cid == "info":
            embed = discord.Embed(title="ℹ Информация о проекте Ordium", description="...", color=0x3498db)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif cid == "ticket":
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name="🎫 Тикеты")
            if category is None:
                category = await guild.create_category("🎫 Тикеты")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            channel_name = f"ticket-{interaction.user.name}".lower().replace(" ", "-")
            existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
            if existing_channel:
                await interaction.response.send_message("❗ У тебя уже есть открытый тикет!", ephemeral=True)
                return
            ticket_channel = await guild.create_text_channel(channel_name, overwrites=overwrites, category=category)
            await ticket_channel.send(f"👋 {interaction.user.mention}, добро пожаловать в тикет...")
            await interaction.response.send_message("✅ Тикет создан!", ephemeral=True)

@bot.command()
async def сосал(ctx):
    ответ = random.choice(["✅ Да", "❌ Нет"])
    await ctx.send(f"{ctx.author.mention} {ответ}")

@bot.command()
async def сезон(ctx):
    embed = discord.Embed(title="📅 Текущий сезон: ???", description="???", color=0x8e44ad)
    await ctx.send(embed=embed)

@bot.command()
async def сюжет(ctx):
    embed = discord.Embed(title="📖 Сюжет Ordium", description="НЕИЗВЕСТННННННННННННО\n", color=0xf1c40f)
    await ctx.send(embed=embed)

@bot.command()
async def игроки(ctx):
    embed = discord.Embed(
        title="🎭 Игроки и роли на сервере",
        description="🧙‍♂ *Создатель* — K1tsune667 and Bofolz\n🛡 *Страж* — Максимыч",
        color=0x1abc9c
    )
    await ctx.send(embed=embed)

@bot.command()
async def вики(ctx):
    embed = discord.Embed(
        title="📚 Вики проекта Ordium",
        description="[Перейти к документации](https://example.gitbook.io/ordium)",
        color=0x3498db
    )
    await ctx.send(embed=embed)

@bot.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        await ctx.send("❌ Ты должен находиться в голосовом канале.")
        return
    voice_channel = ctx.author.voice.channel
    vc = ctx.voice_client or await voice_channel.connect()
    if vc.channel != voice_channel:
        await vc.move_to(voice_channel)
    await ctx.send("🔎 Загружаю трек...")
    FFMPEG_OPTIONS = {'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title', 'Без названия')
    vc.stop()
    vc.play(discord.FFmpegPCMAudio(audio_url, **FFMPEG_OPTIONS))
    await ctx.send(f"▶️ Сейчас играет: **{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹ Остановлено и отключено от канала.")
    else:
        await ctx.send("❌ Бот не находится в голосовом канале.")

user_xp = {}

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.name.startswith("ticket-") and message.content.lower() == "закрыть тикет":
        await message.channel.send("🔒 Тикет будет удалён через 5 секунд...")
        await asyncio.sleep(5)
        await message.channel.delete()
    user_id = str(message.author.id)
    user_xp[user_id] = user_xp.get(user_id, 0) + 10
    if user_xp[user_id] % 100 == 0:
        await message.channel.send(f"🎉 {message.author.mention}, ты получил новый уровень! XP: {user_xp[user_id]}")
    await bot.process_commands(message)

@bot.command()
async def xp(ctx, member: discord.Member = None):
    member = member or ctx.author
    xp = user_xp.get(str(member.id), 0)
    await ctx.send(f"🔢 {member.mention}, у тебя {xp} XP.")

@bot.command()
async def помощь(ctx):
    embed = discord.Embed(
        title="📘 Помощь по командам Ordium",
        description="Ниже список всех доступных команд:",
        color=0x00bcd4
    )
    embed.add_field(name="📅 !сезон", value="Показывает текущий сезон.", inline=False)
    embed.add_field(name="📖 !сюжет", value="Показывает краткий сюжет сервера.", inline=False)
    embed.add_field(name="🎭 !игроки", value="Показывает роли игроков.", inline=False)
    embed.add_field(name="📚 !вики", value="Ссылка на вики-документацию проекта.", inline=False)
    embed.add_field(name="🎶 !play [ссылка]", value="Воспроизводит музыку с YouTube.", inline=False)
    embed.add_field(name="⏹ !stop", value="Останавливает музыку и выходит из голосового канала.", inline=False)
    embed.add_field(name="🔢 !xp", value="Показывает твой опыт (XP).", inline=False)
    embed.add_field(name="😂 !сосал", value="50/50 мемная команда (да/нет).", inline=False)
    embed.add_field(name="🧪 !тест", value="Проверка связи с ботом.", inline=False)
    embed.set_footer(text="Ordium • Последнее обновление: 29.06.2025")
    await ctx.send(embed=embed)

keep_alive()
import os
bot.run(os.getenv("TOKEN"))
