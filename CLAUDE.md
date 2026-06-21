# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the bot

```bash
python index.py
```

Requires a `.env` file in the project root with:
```
TOKEN=<discord_bot_token>
TEST_GUILD_ID=<guild_id>   # optional; omit for global slash command sync
```

Install dependencies:
```bash
pip install discord.py python-dotenv
```

## Architecture

The bot uses `discord.py` with slash commands (`app_commands`) and the Cog system. Entry point is `index.py`, which initializes the bot and calls `load_commands` / `load_events` from `config/loader.py`.

**Auto-loading system** (`config/loader.py`):
- `load_commands(bot)` — walks the `commands/` directory recursively, loading every `.py` file (except `__init__.py`) as a bot extension via `bot.load_extension(module)`.
- `load_events(bot)` — same pattern but only for top-level files in `events/`.
- Each command file must export an `async def setup(bot)` function that calls `await bot.add_cog(...)`.

**Directory layout:**
- `commands/` — slash command Cogs, organized by category (e.g. `commands/admin/`)
- `events/` — event listener Cogs (`ready.py`, `errors.py`)
- `config/` — shared utilities: settings, embed builders, error handling
- `data/` — JSON persistence files (`characters.json`, `clans.json`, `personajes.json`)

**Error handling pipeline:**
- `config/errors.py` — `ErrorType` enum with named error categories
- `config/error_handler.py` — `handle_error(ctx, ErrorType)` builds and sends an embed; works with both `discord.Interaction` (slash) and prefix `ctx`
- `config/error_sender.py` — `send(ctx, embed)` abstraction over interaction vs. prefix context
- `config/embeds.py` — `success_embed`, `error_embed`, `info_embed`, `warning_embed` factory functions

## Adding a new command

1. Create a `.py` file anywhere under `commands/` (or a new subfolder).
2. Define a `commands.Cog` subclass with `@app_commands.command` methods.
3. Add `async def setup(bot): await bot.add_cog(YourCog(bot))` at the bottom.
4. The auto-loader picks it up automatically on next bot start.

Use `handle_error(interaction, ErrorType.X)` for consistent error embeds. Use `success_embed` / `info_embed` from `config/embeds.py` for success responses.

## RPG character system

The bot has a Naruto-themed RPG layer:
- Characters are stored per Discord user ID in `data/characters.json`.
- Clans and their natural elements live in `data/clans.json`.
- `/create-pj` opens a Modal → gender Select → clan Select flow, then saves the generated character with randomized attributes (race, elements based on clan).
- Character creation requires admin approval (`estado_aprobacion: "pendiente"`).
- `config/character.py` and `commands/create_characters.py` both define load/save helpers — prefer the ones in `commands/create_characters.py` as they are more complete.
