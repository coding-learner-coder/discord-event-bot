import discord
from discord.ext import commands, tasks
from discord import app_commands
from datetime import datetime, timedelta
import pytz
import aiosqlite

TOKEN = "MTQ1MDkwMTg2MDEzMDIzMDQ5Nw.GfqAxG.PIUx9xiWWt69zAGmtrbyJ0vgILneo-kkfAuSIcpython"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

UTC = pytz.UTC
ANCHOR_TIME = datetime(2025, 1, 1, 23, 0, tzinfo=UTC)

# ---------------- DATABASE ----------------

async def setup_db():
    async with aiosqlite.connect("events.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS config (
            guild_id INTEGER PRIMARY KEY,
            channel_id INTEGER,
            role_id INTEGER,
            enabled INTEGER
        )
        """)
        await db.commit()

# ---------------- TIME LOGIC ----------------

def next_event_utc(now):
    minutes = int((now - ANCHOR_TIME).total_seconds() // 60)
    next_minutes = ((minutes // 180) + 1) * 180
    return ANCHOR_TIME + timedelta(minutes=next_minutes)

def is_exact_event_time(now):
    return now == next_event_utc(now - timedelta(minutes=1))

# ---------------- AUTO DELETE ----------------

async def auto_delete(msg: discord.Message, delay=600):
    await discord.utils.sleep_until(
        datetime.now(UTC) + timedelta(seconds=delay)
    )
    try:
        await msg.delete()
    except:
        pass

# ---------------- EVENT LOOP ----------------

@tasks.loop(minutes=1)
async def event_loop():
    now = datetime.now(UTC).replace(second=0, microsecond=0)
    next_evt = next_event_utc(now)
    minutes_left = int((next_evt - now).total_seconds() // 60)

    async with aiosqlite.connect("events.db") as db:
        async with db.execute(
            "SELECT guild_id, channel_id, role_id FROM config WHERE enabled = 1"
        ) as cursor:
            rows = await cursor.fetchall()

    for guild_id, channel_id, role_id in rows:
        guild = bot.get_guild(guild_id)
        if not guild:
            continue

        channel = guild.get_channel(channel_id)
        role = guild.get_role(role_id)
        if not channel or not role:
            continue

        # ----- WARNINGS -----
        if minutes_left in (10, 5):
            msg = await channel.send(
                f"⚠️ {role.mention} **Event starts in {minutes_left} minutes**\n"
                f"⏰ <t:{int(next_evt.timestamp())}:R>"
            )
            bot.loop.create_task(auto_delete(msg))

        # ----- EVENT START -----
        if minutes_left == 0:
            msg = await channel.send(
                f"🔔 {role.mention} **Event is starting now!**\n"
                f"⏭ Next event: <t:{int(next_event_utc(now).timestamp())}:R>"
            )
            bot.loop.create_task(auto_delete(msg))

# ---------------- SLASH COMMANDS ----------------

@bot.tree.command(name="enable_events", description="Enable 3-hour event (23:00 GMT anchor)")
@app_commands.describe(channel="Channel to post in", role="Role to ping")
async def enable_events(interaction: discord.Interaction, channel: discord.TextChannel, role: discord.Role):
    async with aiosqlite.connect("events.db") as db:
        await db.execute("""
        INSERT INTO config (guild_id, channel_id, role_id, enabled)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(guild_id) DO UPDATE SET
            channel_id = excluded.channel_id,
            role_id = excluded.role_id,
            enabled = 1
        """, (interaction.guild.id, channel.id, role.id))
        await db.commit()

    next_evt = next_event_utc(datetime.now(UTC))

    await interaction.response.send_message(
        f"✅ Events enabled\n"
        f"📢 Channel: {channel.mention}\n"
        f"🏷 Role: {role.mention}\n"
        f"⏰ Next event: <t:{int(next_evt.timestamp())}:F>",
        ephemeral=True
    )

@bot.tree.command(name="disable_events", description="Disable events")
async def disable_events(interaction: discord.Interaction):
    async with aiosqlite.connect("events.db") as db:
        await db.execute(
            "UPDATE config SET enabled = 0 WHERE guild_id = ?",
            (interaction.guild.id,)
        )
        await db.commit()

    await interaction.response.send_message("⛔ Events disabled.", ephemeral=True)

bot.run(TOKEN)
