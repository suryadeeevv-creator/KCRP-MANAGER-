import aiosqlite

DATABASE = "data/database.db"


async def setup_database():
    async with aiosqlite.connect(DATABASE) as db:

        # Server Settings
        await db.execute("""
        CREATE TABLE IF NOT EXISTS guild_settings(
            guild_id INTEGER PRIMARY KEY,
            ticket_category INTEGER,
            transcript_channel INTEGER,
            staff_role INTEGER,
            ticket_count INTEGER DEFAULT 0
        )
        """)

        # Tickets
        await db.execute("""
        CREATE TABLE IF NOT EXISTS tickets(
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            channel_id INTEGER,
            owner_id INTEGER,
            claimed_by INTEGER,
            status TEXT DEFAULT 'open'
        )
        """)

        # Warnings
        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guild_id INTEGER,
            user_id INTEGER,
            moderator_id INTEGER,
            reason TEXT
        )
        """)

        await db.commit()


# ---------------- SETTINGS ---------------- #

async def get_settings(guild_id: int):
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute(
            "SELECT * FROM guild_settings WHERE guild_id = ?",
            (guild_id,)
        )
        return await cursor.fetchone()


async def save_settings(
    guild_id: int,
    ticket_category: int,
    transcript_channel: int,
    staff_role: int
):
    async with aiosqlite.connect(DATABASE) as db:

        await db.execute("""
        INSERT OR REPLACE INTO guild_settings(
            guild_id,
            ticket_category,
            transcript_channel,
            staff_role
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            guild_id,
            ticket_category,
            transcript_channel,
            staff_role
        ))

        await db.commit()


