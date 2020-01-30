from mwt import MWT
from functools import wraps
import json
from config import config

# Returns a list of admin IDs for a given chat. Results are cached for 15 min.
@MWT(timeout=60*15)
def get_admin_ids(bot, chat_id=None):
    if chat_id is None:
        ids = config["master"]
    else:
        ids = [admin.user.id for admin in bot.get_chat_administrators(chat_id)]
        with open('config/config.json', "r+") as f:
            config["master"] = ids
            json.dump(config, f, indent=4)
    return ids


def send_action(action):
    """Sends `action` while processing func command."""
    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)
        return command_func
    return decorator


def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

