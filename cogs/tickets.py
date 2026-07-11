import discord
from discord.ext import commands
from discord import app_commands

CATEGORY_ID = 1525599685815832616

STAFF_ROLE_IDS = [
    1523613557424521290,  # Founder
    1523613557424521288,  # Server Administrator
    1523613557424521287,  # Server Management
    1523897763484401806,  # Owner
    1523613557424521292,  # Senior Admin
    1523616970824482826,  # General Admin
    1523613557424521289,  # Helper Admin
    1523897469568680066,  # Co Owner
]


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

        guild = interaction.guild
        category = guild.get_channel(CATEGORY_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        }

        for role_id in STAFF_ROLE_IDS:
            role = guild.get_role(role_id)
            if role:
                overwrites[role] = discord.PermissionOverwrite(
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True
                )

        channel = await guild.create_text_channel(
            name=f"ticket-{interaction.user.name}",
            category=category,
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎫 Ticket Created",
            description=(
                f"Hello {interaction.user.mention},\n\n"
                "Your support ticket has been created successfully.\n\n"
                "Please describe your issue in detail.\n\n"
                "A member of the **KCRP Staff Team** will assist you as soon as possible.\n\n"
                "Thank you for your patience. 💚"
            ),
            color=0x57F287
        )

        await channel.send(embed=embed)

        await interaction.response.send_message(
            f"✅ Ticket created: {channel.mention}",
            ephemeral=True
        )


class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="ticket-panel",
        description="Create the ticket panel."
    )
    async def ticket_panel(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🎫 KCRP Support",
            description=(
                "Click the button below to create a support ticket."
            ),
            color=0x57F287
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketView()
        )await interaction.response.send_message(
            embed=embed,
            view=TicketView()
        )async def setup(bot):
    await bot.add_cog(Tickets(bot))
        async def setup(bot):
    await bot.add_cog(Tickets(bot))
