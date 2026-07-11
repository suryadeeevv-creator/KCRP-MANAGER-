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

    category = guild.get_channel(1525599685815832616)

    founder_role = guild.get_role(1523613557424521290)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        ),
        founder_role: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        )
    }

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
        f"✅ Your ticket has been created: {channel.mention}",
        ephemeral=True
    )
