import asyncio
import aiosqlite
import discord
from discord.ext import commands
from discord import app_commands

DATABASE = "data/database.db"

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
async def user_has_ticket(guild_id: int, user_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            """
            SELECT channel_id
            FROM tickets
            WHERE guild_id = ?
            AND owner_id = ?
            AND status = 'open'
            """,
            (guild_id, user_id)
        )

        return await cursor.fetchone()


async def create_ticket_db(
    guild_id: int,
    channel_id: int,
    owner_id: int
):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            """
            INSERT INTO tickets(
                guild_id,
                channel_id,
                owner_id,
                status
            )
            VALUES(?, ?, ?, 'open')
            """,
            (
                guild_id,
                channel_id,
                owner_id
            )
        )

        await db.commit()


async def close_ticket_db(channel_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute(
            """
            UPDATE tickets
            SET status='closed'
            WHERE channel_id=?
            """,
            (channel_id,)
        )

        await db.commit()
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Close Ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒"
    )
    async def close_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "🔒 Closing ticket in 5 seconds...",
            ephemeral=True
        )

        await asyncio.sleep(5)
        await interaction.channel.delete()

async def user_has_ticket(guild, user):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT channel_id FROM tickets WHERE owner_id=? AND status='open'",
            (user.id,)
        )

        ticket = await cursor.fetchone()

        if ticket:
            channel = guild.get_channel(ticket[0])
            if channel:
                return channel

    return None
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

        existing = await user_has_ticket(guild.id, interaction.user.id)

if existing:
    channel = guild.get_channel(existing[0])

    if channel:
        await interaction.response.send_message(
            f"❌ You already have an open ticket: {channel.mention}",
            ephemeral=True
        )
        return

channel = await guild.create_text_channel(
    name=f"ticket-{interaction.user.name.lower()}",
    category=category,
    overwrites=overwrites
)

await create_ticket_db(
    guild.id,
    channel.id,
    interaction.user.id
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

await channel.send(
    embed=embed,
    view=CloseTicketView()
)

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
            description="Click the button below to create a support ticket.",
            color=0x57F287
        )

        await interaction.response.send_message(
            embed=embed,
            view=TicketView()
        )


async def setup(bot):
    await bot.add_cog(Tickets(bot))
