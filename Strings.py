class Global:
    user_not_exist = "you don't exist in my database. Start me in your LGS group\n"
    user_already_exist = "you already exist in my database"
    welcome = "welcome :)"


class Dci:
    dci_set = "Done! Your DCI number is set to {}"
    dci_invalid = "hey something went wrong. \nUsage: `/dci` 11223344"


class Name:
    name_set = "Your player name is now set to {}"
    name_invalid = "hey something went wrong. \nUsage: `/name` yourname"


class Arena:
    arena_set = "your MTGArena player name is now set to {}"
    arena_invalid = "hey something went wrong. \nUsage: `/arena` yourname"


class Start:
    start_pvt = "You are successfully registered on this bot :)\n"
    start_id = "your telegram ID is `{}`"


class Card:
    card_not_found = "No card found with name _{}_"
    card_legal = "legal everywhere"
    card_unavailable = "N.A."
    card_ruling_unavailable = "no rules available for this card"


class Help:
    admin_help = "Hello admin!"
    user_help = "This bot is a work in progress and because of that, not all commands are documented.\n" \
                "This bot is intended to be used inside a group, so please start it in your local MTG group!"
    admin_commands = ""
    user_commands = ""


class Log:
    database_not_found = "database not found! Generating a new one..."
    database_ready = "database found"
    database_ok = "database generated."
    cached = "using cached value"
    new_cache = "new value cached"


class Inline:
    player_card_text = "Hello {}!\n*telegram ID:* `{}`\n*DCI number:* `{}`\n*Arena nickname:* _{}_"
    player_card_desc = "your player card: dci, arena nickname..."
    player_card_title = "Player card"

