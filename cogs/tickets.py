import discord
from discord.ext import commands
from discord import app_commands

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ticket-panel",
        description="Create the KCRP ticket panel."
    )
    async def ticket_panel(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎫 KCRP Support",
            description=(
                "Need help?\n\n"
                "Click the **Create Ticket** button below.\n"
                "Our staff will assist you as soon as possible."
            ),
            color=0x57F287
        )

        embed.set_footer(text="KCRP Manager")

        await interaction.response.send_message(
            embed=embed,
            view=TicketView()
        )

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Create Ticket",
        emoji="🎫",
        style=discord.ButtonStyle.green
    )
    async def create_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "🚧 Ticket system is coming in the next step!",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Tickets(bot))
