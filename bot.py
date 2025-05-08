#!/usr/bin/python3
"""Discord bot for getting Bible verses."""

from os import environ
from typing import Optional

import discord
from discord import app_commands
#from icecream import ic
from pylsb.bible import BibleGetter, BibleMarker
from pylsb.data import BOOKS, TITLES
from pylsb.parse import get_scripture
from pylsb_cli.bible_format import bible_label

TOKEN = environ.get('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
# bot = commands.Bot(command_prefix='$', intents=intents)
tree = app_commands.CommandTree(client)

# For PyLSB
bible = BibleGetter('./cache/lsbible.json')


async def translation_autocomplete(
    interaction: discord.Interaction,
    current: str
) -> list[app_commands.Choice[str]]:
    """Autocompletion for /scripture translation option."""
    versions = ['LSB', 'ESV']
    return [
        app_commands.Choice(name=version, value=version.lower())
        for version in versions
        if current.lower() in version.lower()
    ]


@tree.command(name='scripture', description='Get verses from the Bible.')
@app_commands.autocomplete(translation=translation_autocomplete)
async def scripture(
    interaction: discord.Interaction,
    query: str,
    translation: Optional[str]='lsb'
):
    """Test parsing of arguments."""
    res = None
    try:
        res = get_scripture(query, bible)
        # await interaction.response.send_message(
        #     f"Got {bible_label(res) if res else 'nothing'}\nTranslation: {translation}")
    except ValueError as _e:
        return await interaction.response.send_message(
            f"Error: `{'` matches'.join(_e.args[0].rsplit(' matches', 1))}",
            ephemeral=True)

    if not res:
        return await interaction.response.send_message(
            f'Invalid Scripture request: {query}',
            ephemeral=True)
    # get bible_label(res)

    reply = f'**{bible_label(res)}**\n> '
    match translation:
        case 'lsb':
            data = bible.get(res, False)
            if not data:
                return await interaction.response.send_message(
                    'Invalid Bible ' +
                    ('verse' if isinstance(res, BibleMarker) else 'verses') +
                    f': {bible_label(res)}\n',
                    ephemeral=True)
            #ic(data)
            # Between books
            addition = '\n\n'.join([
                # Between chapters
                '\n'.join([
                    # Between verses
                    ' '.join([
                        (f'## {"\n## ".join(TITLES[BOOKS.index(book_title)].split("\n"))}' if chapter_number == 1 and verse_number == 1 else '') +
                        (f'\n### {verse["heading"]}\n' if verse["heading"] else '') +
                        f'[{verse_number}] {
                            (" ".join(verse["text"]))
                            .replace("\x1b[31m", "**")
                            .replace("\x1b[39m", "**")
                            .replace("\x1b[3m", "*")
                            .replace(" \x1b[23m", "* ")}'
                        for verse_number, verse in chapter.items()
                    ])
                    for chapter_number, chapter in book.items()
                ])
                for book_title, book in data.items()
            ]).replace('\n', '\n> ')
            if addition.startswith('\n> '):
                addition = addition[3:]
            reply += addition
        case 'esv':
            await interaction.response.send_message(
                'not implemented yet',
                ephemeral=True)

    # Reply
    try:
        await interaction.response.send_message(reply)
    except discord.errors.HTTPException as _e:
        if '2000 or fewer' in _e.text:
            return await interaction.response.send_message(
                'data too long',
                ephemeral=True)
        raise _e


@client.event
async def on_ready():
    """To run on login."""
    await tree.sync()
    print(f'Logged in as {client.user}.')


client.run(TOKEN)
