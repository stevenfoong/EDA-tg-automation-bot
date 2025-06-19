import json
import os
import logging

logger = logging.getLogger(__name__)

PERMISSIONS_FILE = os.getenv("PERMISSIONS_FILE", "data/permissions.json")

def load_permissions():
    with open(PERMISSIONS_FILE, "r") as f:
        return json.load(f)

def get_allowed_commands(chat_id, user_id):
    perms = load_permissions()
    # Get allowed commands from both user and group
    user_allowed = perms.get("users", {}).get(str(user_id), [])
    group_allowed = perms.get("groups", {}).get(str(chat_id), [])
    # Return union (unique set)
    return list(set(user_allowed) | set(group_allowed))

def is_command_allowed(chat_id, user_id, command):
    if command == "get_id":
        return True
    allowed = get_allowed_commands(chat_id, user_id)
    return command in allowed


