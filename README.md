<h1 align="center"> Discord Bot Template </h1>

<p align="center">
A production-ready Discord bot template with modular feature management, modern development tools, and best practices.
</p>

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![discord.py](https://img.shields.io/badge/discord.py-2.6.4+-blue.svg)
![uv](https://img.shields.io/badge/uv-package_manager-purple.svg)
![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

## ✨ Highlights

- **🎯 Modular Feature System** — Enable/disable features and cogs with simple configuration
- **🤖 Discord.py 2.6.4+** — Built on the latest discord.py with full slash command support
- **⚡ Ultra-fast Setup** — Get your bot running in minutes with `uv` package manager
- **🏗️ Organized Structure** — Clean separation of features, events, components, and tasks
- **🔧 Developer Experience** — Hot reload, linting, formatting, and type checking out of the box

## 🚀 Key Features

- **Python 3.10+** with modern async/await patterns
- **[discord.py](https://discordpy.readthedocs.io/)** — Full-featured Discord API wrapper with slash commands
- **[uv](https://docs.astral.sh/uv/)** — Ultra-fast Python package installer and dependency resolver
- **Modular Architecture** — Organize your bot into features, easily enable/disable them
- **[Docker Support](https://docs.docker.com/)** — Containerized development and deployment
- **[Code Quality Tools](https://docs.astral.sh/ruff/)** — Linting with [Ruff](https://docs.astral.sh/ruff/), type checking with [MyPy](https://mypy.readthedocs.io/)
- **[Pre-commit Hooks](https://pre-commit.com/)** — Automated code quality checks before every commit
- **[Commitizen](https://commitizen-tools.github.io/commitizen/)** — Standardized commits and automated versioning
- **Structured Logging** — Colorful, informative logs with configurable levels
- **Environment Management** — Clean configuration with environment variables
- **[Makefile Automation](https://www.gnu.org/software/make/)** — Simple commands for common tasks

## 📁 Project Structure

```
discord-bot-template/
├── src/
│   ├── bot/
│   │   ├── client.py           # Custom bot client with optimization
│   │   ├── setup.py            # 🎯 Main feature control center
│   │   ├── features/           # Feature-based cogs
│   │   │   └── meta/           # Example: Meta feature (ping, info, etc.)
│   │   │       ├── setup.py    # Feature-level control
│   │   │       └── commands/
│   │   │           ├── __init__.py  # Cog-level control
│   │   │           └── ping.py      # Individual cog
│   │   ├── events/             # Event listener cogs
│   │   ├── components/         # UI components (buttons, modals, etc.)
│   │   └── tasks/              # Background tasks
│   ├── config/                 # Configuration management
│   └── utils/                  # Shared utilities
├── __main__.py                 # Application entry point
├── .env.example                # Environment variables template
├── pyproject.toml              # Project dependencies and tools config
├── Makefile                    # Development workflow automation
├── FEATURE_MANAGEMENT.md       # 📖 Feature system guide
└── SETUP_SUMMARY.md            # Quick reference
```

## 📋 Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv) package manager
- Discord Bot Token ([Get one here](https://discord.com/developers/applications))
- Docker (optional, for containerized development)
- Git

## ⚡ Quick Start

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd discord-bot-template
```

### 2️⃣ Initialize the Project
```bash
make init
```
This will:
- Install all dependencies using uv
- Set up pre-commit hooks

### 3️⃣ Configure Your Bot
```bash
cp .env.example .env
```

Edit `.env` and add your Discord bot token:
```env
BOT_TOKEN=your-discord-bot-token-here
```

> **💡 How to get a bot token:**
> 1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
> 2. Create a New Application
> 3. Go to the "Bot" section
> 4. Click "Reset Token" and copy it
> 5. Enable required intents (Presence, Server Members, Message Content)

### 4️⃣ Run Your Bot
```bash
make run
```

Your bot is now online! 🎉

## 🎯 Feature Management

This template uses a powerful modular system that lets you easily manage features and cogs.

### Quick Examples

**Disable an entire feature** — Edit `src/bot/setup.py`:
```python
enabled_features = {
    "meta": False,  # ❌ Disabled
}
```

**Disable a specific cog** — Edit `src/bot/features/meta/commands/__init__.py`:
```python
COGS = [
    # "src.bot.features.meta.commands.ping",  # ❌ Commented out
]
```

**Disable event listeners** — Edit `src/bot/events/__init__.py`:
```python
COGS = [
    # "src.bot.events.on_message",  # ❌ Disabled
]
```

**📖 For detailed guide, see [FEATURE_MANAGEMENT.md](FEATURE_MANAGEMENT.md)**

## 🏗️ Creating Your First Feature

### 1. Create the feature structure:
```bash
mkdir -p src/bot/features/moderation/commands
```

### 2. Create `setup.py`:
```python
# src/bot/features/moderation/setup.py
from src.bot.features.moderation.commands import get_cogs as get_command_cogs

COGS = [*get_command_cogs()]

def get_cogs() -> list[str]:
    return COGS
```

### 3. Create cog list:
```python
# src/bot/features/moderation/commands/__init__.py
COGS = [
    "src.bot.features.moderation.commands.kick",
    "src.bot.features.moderation.commands.ban",
]

def get_cogs() -> list[str]:
    return COGS
```

### 4. Create your cog:
```python
# src/bot/features/moderation/commands/kick.py
from typing import TYPE_CHECKING
from discord import app_commands, Member
from discord.ext.commands import Cog
from discord.interactions import Interaction

if TYPE_CHECKING:
    from src.bot.client import CustomBot

class Kick(Cog):
    def __init__(self, bot: "CustomBot") -> None:
        self.bot = bot

    @app_commands.command(name="kick")
    async def kick(self, interaction: Interaction, member: Member):
        """Kick a member from the server."""
        await interaction.response.send_message(
            f"Kicked {member.mention}"
        )

async def setup(bot: "CustomBot") -> None:
    await bot.add_cog(Kick(bot))
```

### 5. Enable in `src/bot/setup.py`:
```python
from src.bot.features.moderation.setup import get_cogs as get_moderation_cogs

enabled_features = {
    "meta": True,
    "moderation": True,  # ✅ Enable your feature
}

# ... in the collection section:
if enabled_features.get("moderation", False):
    cog_modules.extend(get_moderation_cogs())
```

## 🛠️ Development Commands

```bash
make run         # Run the bot locally
make lint        # Run linter (Ruff)
make format      # Format code (Ruff)
make typecheck   # Run type checker (MyPy)
make clean       # Clean up cache files
make commit      # Commit with conventional commit message
make bump        # Bump version and update changelog
```

## 🐳 Docker Development

### Build and run with Docker Compose:
```bash
make dev-build   # Build the container
make dev-up      # Start the container
make dev-logs    # View logs
make dev-exec    # Execute commands in container
make dev-down    # Stop and remove container
```

### Quick Docker run:
```bash
docker compose --env-file=.env up --build
```

## 📚 Documentation

- **[discord.py Documentation](https://discordpy.readthedocs.io/)** — Official discord.py docs

## 📄 License
[MIT License](./LICENSE) — Yurii | monok8i 🦋
