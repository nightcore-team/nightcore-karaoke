#!/usr/bin/env bash

set -e

# Run database migrations
alembic upgrade head

# Start the bot
python __main__.py
