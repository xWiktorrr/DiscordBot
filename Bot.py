import discord
from discord.ext import commands
import json
import os
from datetime import datetime


TOKEN = "MTQ5ODIwNzIxMTQyNjU0NTY4NQ.GPDWlM.Rth08JcNS-Po00rSF63ziflOpIPvG51VjF-hxM"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

DATA_FILE = "data.json"
MESSAGE_FILE = "message_id.txt"

RACE_TIME = datetime(2026, 5, 2, 18, 0)
CLOSE_TIME = datetime(2026, 5, 2, 15, 0)

RACE_TIMESTAMP = int(RACE_TIME.timestamp())
CLOSE_TIMESTAMP = int(CLOSE_TIME.timestamp())

ADMIN_ROLE = "Owner"

TEAM_ROLES = {
    "Alpine": 1488178984637304902,
    "AstonMartin": 1488178554406436886,
    "Ferrari": 1488179083513823412,
    "Haas": 1488179133266792518,
    "Sauber": 1488178804273844354,
    "McLaren": 1488178864772485150,
    "Mercedes": 1488178500274749680,
    "Vcarb": 1488178604478304306,
    "RedBull": 1488178657565474937,
    "Williams": 1488179042732605440
}

TEAM_EMOJIS = {
    "Alpine": 1498237317532618762,
    "AstonMartin": 1498237595556249732,
    "Ferrari": 1498236681596305549,
    "Haas": 1498240762968674385,
    "Sauber": 1498241295205011526,
    "McLaren": 1498240528360149002,
    "Mercedes": 1498226182544691341,
    "Vcarb": 1498239868495462514,
    "RedBull": 1498239486365012129,
    "Williams": 1498240098859221052
}

default_data = {
    "Alpine": {"limit": 2, "players": []},
    "AstonMartin": {"limit": 2, "players": []},
    "Ferrari": {"limit": 2, "players": []},
    "Haas": {"limit": 2, "players": []},
    "Sauber": {"limit": 2, "players": []},
    "McLaren": {"limit": 2, "players": []},
    "Mercedes": {"limit": 2, "players": []},
    "Vcarb": {"limit": 2, "players": []},
    "RedBull": {"limit": 2, "players": []},
    "Williams": {"limit": 2, "players": []},
    "Rezerwa": {"limit": 99, "players": []},
    "Nie jadę": {"limit": 99, "players": []}
}

# 📂 dane
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(default_data, f, indent=4)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_message_id(mid):
    with open(MESSAGE_FILE, "w") as f:
        f.write(str(mid))

def load_message_id():
    if not os.path.exists(MESSAGE_FILE):
        return None
    with open(MESSAGE_FILE, "r") as f:
        return int(f.read())

# 🎨 embed
def generate_embed(data):
    desc = ""

    sorted_teams = sorted(
        data.items(),
        key=lambda x: len(x[1]["players"]),
        reverse=True
    )

    for team, info in sorted_teams:
        emoji_id = TEAM_EMOJIS.get(team)
        emoji = f"<:x:{emoji_id}>" if emoji_id else ""

        desc += f"{emoji} **{team} ({len(info['players'])}/{info['limit']})**\n"

        if not info["players"]:
            desc += "-\n\n"
        else:
            for p in info["players"]:
                desc += f"{p}\n"
            desc += "\n"

    embed = discord.Embed(
        title="🏁 ROUND 3: MONZA 🇮🇹",
        description=(
            "🟩⬜🟥 **GP WŁOCH** 🟩⬜🟥\n\n"
            f"📅 <t:{RACE_TIMESTAMP}:F>\n"
            f"⏳ Zapisy zamykają się: <t:{CLOSE_TIMESTAMP}:R>\n\n"
            f"{desc}"
        ),
        color=discord.Color.dark_purple()
    )

    embed.set_image(
        url="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhgrRQAylS892x9CmOaBLY6At_D-JZyz3kiTAUuVdttHrkzwMjYNM3myPTk1A23YCjPD3QtNWR-YLiLF61h18EUGqiP5P2KXwcjRK4nc5nJ_kE4dCjwHVepJeSuG0jEG_neU9p3i-DVnVEgovm_HBXYneNkS7KYtryMDhdQJ_8tH86JPdsmEC2TyirlyfI/s884/Autodromo%20Nazionale%20Monza.png"
    )

    return embed

# 🔘 UI
class TeamView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        data = load_data()
        for team in data:
            self.add_item(TeamButton(team))

class TeamButton(discord.ui.Button):
    def __init__(self, team):
        emoji_id = TEAM_EMOJIS.get(team)
        emoji = discord.utils.get(bot.emojis, id=emoji_id) if emoji_id else None

        super().__init__(
            label=team,
            style=discord.ButtonStyle.primary,
            emoji=emoji
        )

        self.team = team

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        if datetime.now() > RACE_TIME:
            await interaction.response.send_message("⛔ Zapisy zamknięte!", ephemeral=True)
            return

        team_role_id = TEAM_ROLES.get(self.team)
        has_role = any(role.id == team_role_id for role in user.roles)

        if not has_role:
            await interaction.response.send_message(
                "❌ Możesz zapisać się tylko do swojej drużyny!",
                ephemeral=True
            )
            return

        data = load_data()
        team_data = data[self.team]
        players = "\n".join(team_data["players"]) or "Brak"
        user = str(interaction.user)

        # znajdź gdzie jest user
        current_team = None
        for t in data:
            if user in data[t]["players"]:
                current_team = t
                break
        #blokada, jedna drużyna dla jednego użytkownika
        if current_team and current_team != self.team:
            await interaction.response.send_message(
                "❌ Możesz być tylko w jednej drużynie!",
                ephemeral=True
            )
            return

        # toggle
        if current_team == self.team:
            data[self.team]["players"].remove(user)
            save_data(data)
            await interaction.response.send_message(f"❌ Wypisałeś się z {self.team}", ephemeral=True)

        else:
            if current_team:
                data[current_team]["players"].remove(user)

            if len(data[self.team]["players"]) >= data[self.team]["limit"]:
                await interaction.response.send_message("❌ Team pełny!", ephemeral=True)
                return

            data[self.team]["players"].append(user)
            save_data(data)

            await interaction.response.send_message(f"✅ Dołączyłeś do {self.team}", ephemeral=True)

        await interaction.message.edit(
            embed=generate_embed(data),
            view=TeamView()
        )

# 📢 komenda
@bot.command(name="obecność")
@commands.has_role("Owner")
async def obecność(ctx):
    data = load_data()
    embed = generate_embed(data)

    mid = load_message_id()

    if mid:
        try:
            msg = await ctx.channel.fetch_message(mid)
            await msg.edit(embed=embed, view=TeamView())
            await ctx.send("✅ Zaktualizowano", delete_after=3)
            return
        except:
            pass

    msg = await ctx.send(embed=embed, view=TeamView())
    save_message_id(msg.id)

# 👑 admin
def is_admin(ctx):
    return any(role.name == ADMIN_ROLE for role in ctx.author.roles)

@bot.command()
@commands.has_role("Owner")
async def reset(ctx):
    if not is_admin(ctx):
        return
    save_data(default_data)
    await ctx.send("♻️ Reset")

@bot.command()
@commands.has_role("Owner")
async def clear(ctx, *, team):
    if not is_admin(ctx):
        return
    data = load_data()
    if team in data:
        data[team]["players"] = []
        save_data(data)
        await ctx.send(f"🧹 Wyczyszczono {team}")

@bot.command()
@commands.has_role("Owner")
async def help(ctx):
    embed = discord.Embed(
        title="🏁 VELOCITY GRID BOT",
        description="📋 Dostępne komendy:",
        color=0xff0000
    )

    embed.add_field(
        name="📊 !obecność",
        value="Wyświetla panel zapisów",
        inline=False
    )

    embed.add_field(
        name="♻️ !reset",
        value="Resetuje listę obecności",
        inline=False
    )

    embed.add_field(
        name="❓ !help",
        value="Pokazuje tę wiadomość",
        inline=False
    )

    embed.set_footer(text="Velocity Grid • System zapisów")

    await ctx.send(embed=embed)

# 🧠 start
@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user}")
    load_data()

bot.run(TOKEN)