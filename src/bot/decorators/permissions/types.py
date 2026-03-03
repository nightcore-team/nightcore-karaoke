"""Permissions enums for the bot."""

from enum import Enum


class PermissionFlagEnum(str, Enum):
    """Enum representing permission flags."""

    NONE = "nonetype"
    BOT_ACCESS = "bot_access"
    KARAOKE_CONFIG_ACCESS = "karaoke_config_access"
    HOST_ACCESS = "host_access"
    JUDGE_ACCESS = "judge_access"
    UNSAFE = "unsafe"
