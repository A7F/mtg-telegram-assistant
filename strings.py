class Global:
    user_not_exist = "you don't exist in my database. Start me in your LGS group\n"
    user_already_exist = "you already exist in my database"
    welcome_message = "Hello {} and welcome in our group! :smile:\n_Have fun!_"
    format_banlist = "Click here to go to the official banlist page"


class Friendlist:
    friendlist = "This is the friendlist"
    refresh = "refresh"


class Dci:
    dci_set = "Done! Your DCI number is set to {}"
    dci_invalid = "hey something went wrong. \nUsage: `/dci` 11223344"


class Name:
    name_set = "Your player name is now set to {}"
    name_invalid = "hey something went wrong. \nUsage: `/name` yourname"


class Arena:
    arena_set = "your MTGArena player name is now set to {}"
    arena_invalid = "hey something went wrong. \nUsage: `/arena` yourname"
    arena_status = "_MTGA state of servers_"
    server_ok = "operational"
    server_maintenance = "under maintenance"
    goto_statuspage = "See more..."


class Start:
    start_pvt = "You are successfully registered on this bot :)\n"
    start_id = "your telegram ID is `{}` and this group id is `{}`"
    welcome = "welcome, fellow planeswalker! You are now registered in my book of spells.\n" \
              "If you need anything, you can ask me help using `/help` via pvt.\n" \
              "Oh, by the way, this group ID is {}. Use it to set up RSS feeds!"


class Card:
    card_not_found = "No card found with name _{}_"
    card_autocorrect = "Maybe you did a typo or the query is too broad.\nDid you mean...?\n\n{}"
    card_legal = "legal everywhere"
    card_unavailable = "N.A."
    card_ruling_unavailable = "no rules available for this card"


class Help:
    social_links = ":rocket: Here are the links for everything related our group! :rocket:\n\n"
    no_social_links = ":rocket: There is currently no social network related to our group. :rocket:"
    admin_help = "Well... there are no admin commands implemented up to now... Sorry!"
    user_help = "*Commands available via PVT (which is, in this chat):*\n\n" \
                "_No parameter commands:_\n" \
                "`/start` - gives you feedback on your registration status and your telegram user ID.\n" \
                "`/help` - get this help text. If you are an admin, it also sends their help text\n\n" \
                "_1 parameter PVT commands. In case you set the wrong value, you can use the related command again:_\n" \
                "`/name` - set your player name which is the name this bot will use to address you\n" \
                "`/dci` - set your dci number. Because is a number, the bot expects a number\n" \
                "`/arena` - set your mtg:arena player name. Useful to let other players challenge you\n\n" \
                "_Inline commands:_\n" \
                "Whenever you summon this bot via inline, if no text is passed, it lets you choose to display your player card." \
                "Your player card consists of your name, your DCI number, your telegram ID and your mtg:arena nickname. Be careful though! " \
                "If you care about your privacy, don't use it in untrusted chats.\n\n"\
                "*Group commands:*\n"\
                "`[[cardname]]` - search for the card named `cardname` on scryfall. Also available via pvt.\n"\
                "`((cardname))` - search for rulings related to the card named `cardname`. Also available via pvt.'\n" \
                "`/status` - check all MTGA servers if are operational or under maintenance\n" \
                "`/friendlist` - get the friendlist.\n" \
                "`/rotation` - check which sets are rotating. Also available via pvt.\n" \
                "`/banlist` - get the link to visit the official banlist page. Also available via pvt.\n" \
                "`/social` - get a list with all the social links for this community. Also available via pvt.\n"


class Log:
    database_not_found = "database not found! Generating a new one..."
    database_ready = "database found"
    database_ok = "database generated."
    cached = "using cached value"
    new_cache = "new value cached"


class Inline:
    player_card_text = "Hello {}!\n" \
                       "*telegram ID:* `{}`\n" \
                       "*DCI number:* `{}`\n" \
                       "*Arena nickname:* _{}_"
    player_card_desc = "your player card: dci, arena nickname..."
    player_card_title = "Player Card"

