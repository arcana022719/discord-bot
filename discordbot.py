import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

STAFF_CHANNEL_ID = 1428374679915069513  # 🔧 Replace this with your private channel ID


class SubmissionModal(discord.ui.Modal, title="Submit Your Entry"):
    ign = discord.ui.TextInput(label="IGN", placeholder="Enter your in-game name")

    image_links = discord.ui.TextInput(
        label="Image Links",
        style=discord.TextStyle.paragraph,
        placeholder="Paste 1–5 image URLs here (one per line)",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        staff_channel = bot.get_channel(STAFF_CHANNEL_ID)

        # Split links into list, remove empty lines/spaces
        urls = [u.strip() for u in self.image_links.value.splitlines() if u.strip()]
        if len(urls) == 0:
            await interaction.response.send_message(
                "❌ You must submit at least one image link.",
                ephemeral=True
            )
            return

        embed = discord.Embed(title="📨 New Submission", color=discord.Color.blurple())
        embed.add_field(name="IGN", value=self.ign.value, inline=False)
        embed.add_field(name="Number of URLs", value=str(len(urls)), inline=True)

        for i, url in enumerate(urls, start=1):
            embed.add_field(name=f"Image {i}", value=url, inline=False)

        embed.set_footer(text=f"Submitted by {interaction.user}")

        await staff_channel.send(embed=embed)
        await interaction.response.send_message(
            f"✅ Submission received! You submitted **{len(urls)}** image link(s).",
            ephemeral=True
        )


class SubmitButton(discord.ui.View):
    @discord.ui.button(label="Submit", style=discord.ButtonStyle.green)
    async def submit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SubmissionModal())


@bot.tree.command(name="post_submission_button", description="Post the submission button in this channel.")
async def post_submission_button(interaction: discord.Interaction):
    view = SubmitButton()
    await interaction.channel.send(
        "**🎯 Submit Your Entry Here!**\nClick the button below to submit your IGN and image links.",
        view=view
    )
    await interaction.response.send_message("✅ Button posted!", ephemeral=True)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(e)


TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ DISCORD_BOT_TOKEN not found in environment variables. Please add it to your .env file.")
bot.run(TOKEN)
