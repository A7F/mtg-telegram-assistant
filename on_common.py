import telegram, scrython, re, asyncio, time, strings, util, logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMediaPhoto
from telegram import ChatAction
from emoji import emojize
from telegram.ext import CallbackContext
from config import max_cards
import cacheable

logger = logging.getLogger(__name__)


@util.send_action(ChatAction.UPLOAD_PHOTO)
def cards(update: Update, context: CallbackContext):
    match = re.findall(r'\[\[(.*?)\]\]', update.message.text)
    asyncio.set_event_loop(asyncio.new_event_loop())
    is_flipcard = False
    photos = []
    button_list = []
    footer_list = []
    header_list = []
    for index, name in enumerate(match):
        if index > max_cards:
            break
        try:
            card = scrython.cards.Named(fuzzy=name)
        except scrython.ScryfallError:
            auto = scrython.cards.Autocomplete(q=name, query=name)
            if len(auto.data()) > 0:
                text = ""
                for index, item in zip(range(5), auto.data()):
                    text += '`{}`\n'.format(item)
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=strings.Card.card_autocorrect.format(text),
                                         parse_mode=telegram.ParseMode.MARKDOWN)
                continue
            else:
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=strings.Card.card_not_found.format(name),
                                         parse_mode=telegram.ParseMode.MARKDOWN)
                continue
        del card.legalities()["penny"]
        del card.legalities()["oldschool"]
        del card.legalities()["future"]
        del card.legalities()["duel"]
        banned_in = [k for k, v in card.legalities().items() if v == "banned" or v == "not_legal"]
        legal_in = [k for k, v in card.legalities().items() if v == "legal"]
        legal_text = ""

        if len(banned_in) == 0:
            legal_text = strings.Card.card_legal
        else:
            footer_list.append(InlineKeyboardButton("Legalities", callback_data=card.name()))
            for v in legal_in:
                legal_text += ':white_check_mark: {}\n'.format(v)
            for v in banned_in:
                legal_text += ':no_entry: {}\n'.format(v)
            cacheable.CACHED_LEGALITIES.update({card.name(): legal_text})

        eur = '{}€'.format(card.prices(mode="eur")) if card.prices(mode="eur") is not None else "CardMarket"
        usd = '{}€'.format(card.prices(mode="usd")) if card.prices(mode="usd") is not None else "TCGPlayer"
        usd_link = card.purchase_uris().get("tcgplayer")
        eur_link = card.purchase_uris().get("cardmarket")
        img_caption = emojize(":moneybag: [" + eur + "]" + "(" + eur_link + ")" + " | "
                              + "[" + usd + "]" + "(" + usd_link + ")" + "\n"
                              + legal_text, use_aliases=True)

        try:
            card.card_faces()[0]['image_uris']
            is_flipcard = True
        except KeyError:
            is_flipcard = False
            pass

        if len(match) > 1 or is_flipcard:
            if is_flipcard:
                photos.append(InputMediaPhoto(media=card.card_faces()[0]['image_uris']['normal'],
                                              caption=img_caption,
                                              parse_mode=telegram.ParseMode.MARKDOWN))
                photos.append(InputMediaPhoto(media=card.card_faces()[1]['image_uris']['normal'],
                                              caption=img_caption,
                                              parse_mode=telegram.ParseMode.MARKDOWN))
            else:
                photos.append(InputMediaPhoto(media=card.image_uris(0, image_type="normal"),
                                              caption=img_caption,
                                              parse_mode=telegram.ParseMode.MARKDOWN))
                time.sleep(0.04)
                continue
        else:
            if card.related_uris().get("edhrec") is not None:
                button_list.append(InlineKeyboardButton("Edhrec", url=card.related_uris().get("edhrec")))
            if card.related_uris().get("mtgtop8") is not None:
                button_list.append(InlineKeyboardButton("Top8", url=card.related_uris().get("mtgtop8")))
            button_list.append(InlineKeyboardButton("Scryfall", url=card.scryfall_uri()))
            if card.prices(mode="usd") is not None:
                header_list.append(InlineKeyboardButton('{}$'.format(card.prices(mode="usd")),
                                                        url=card.purchase_uris().get("tcgplayer")))
            else:
                header_list.append(InlineKeyboardButton("TCGPlayer", url=usd_link))
            if card.prices(mode="eur") is not None:
                header_list.append(InlineKeyboardButton('{}€'.format(card.prices(mode="eur")),
                                                        url=card.purchase_uris().get("cardmarket")))
            else:
                header_list.append(InlineKeyboardButton("MKM", url=eur_link))
            reply_markup = InlineKeyboardMarkup(util.build_menu(button_list,
                                                                header_buttons=header_list,
                                                                footer_buttons=footer_list,
                                                                n_cols=3))
            context.bot.send_photo(chat_id=update.message.chat_id,
                                   photo=card.image_uris(0, image_type="normal"),
                                   parse_mode=telegram.ParseMode.MARKDOWN,
                                   reply_markup=reply_markup,
                                   reply_to_message_id=update.message.message_id)
            return
    if len(match) > 1 or is_flipcard:
        context.bot.send_media_group(chat_id=update.message.chat_id,
                                     media=photos,
                                     reply_to_message_id=update.message.message_id,
                                     disable_notification=True)


@util.send_action(ChatAction.TYPING)
def rulings(update: Update, context: CallbackContext):
    match = re.findall(r'\(\((.*?)\)\)', update.message.text)
    asyncio.set_event_loop(asyncio.new_event_loop())
    for index, name in enumerate(match):
        if index > max_cards:
            break
        try:
            card = scrython.cards.Named(fuzzy=name)
        except Exception:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Card.card_not_found.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
            continue
        rule = scrython.rulings.Id(id=card.id())
        context.bot.send_chat_action(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
        message = ""
        if rule.data_length() == 0:
            message = strings.Card.card_ruling_unavailable
        else:
            for index, rule_text in enumerate(rule.data()):
                message += (str(index + 1) + ". " + rule.data(index=index, key="comment") + "\n\n")
        context.bot.send_message(chat_id=update.message.chat_id, text=message, reply_to_message_id=update.message.message_id)
        time.sleep(0.07)


@util.send_action(ChatAction.TYPING)
def check_rotation(update: Update, context: CallbackContext):
    text = cacheable.build_rotationlist()
    context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def cards_banlist(update: Update, context: CallbackContext):
    text = cacheable.build_banlist()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=text,
                             parse_mode=telegram.ParseMode.MARKDOWN,
                             disable_web_page_preview=True)


def legalities(update: Update, context: CallbackContext):
    query = update.callback_query
    card_name = query.data
    if card_name in cacheable.CACHED_LEGALITIES.keys():
        logger.info(strings.Log.cached)
        context.bot.answer_callback_query(query.id,
                                          emojize(cacheable.CACHED_LEGALITIES[card_name], use_aliases=True),
                                          show_alert=True)
        query.answer()
    else:
        logger.info(strings.Log.new_cache)
        asyncio.set_event_loop(asyncio.new_event_loop())
        card = scrython.cards.Named(exact=card_name)
        del card.legalities()["penny"]
        del card.legalities()["oldschool"]
        del card.legalities()["future"]
        del card.legalities()["duel"]
        banned_in = [k for k, v in card.legalities().items() if v == "banned" or v == "not_legal"]
        legal_in = [k for k, v in card.legalities().items() if v == "legal"]
        legal_text = ""
        if len(banned_in) == 0:
            legal_text = strings.Card.card_legal
        else:
            for v in legal_in:
                legal_text += ':white_check_mark: {}\n'.format(v)
            for v in banned_in:
                legal_text += ':no_entry: {}\n'.format(v)
            cacheable.CACHED_LEGALITIES.update({card.name(): legal_text})
            context.bot.answer_callback_query(query.id,
                                              emojize(cacheable.CACHED_LEGALITIES[card_name], use_aliases=True),
                                              show_alert=True)
            query.answer()
