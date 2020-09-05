import tables, strings, util, telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ChatAction
from peewee import *
from emoji import emojize
from telegram.ext import CallbackContext
import cacheable, json, os
from datetime import date


def start_pvt(update: Update, context: CallbackContext):
    try:
        tables.User.get(tables.User.user_id == update.message.from_user.id)
        text = strings.Start.start_pvt
    except DoesNotExist:
        text = strings.Global.user_not_exist
    finally:
        text += strings.Start.start_id.format(update.message.from_user.id, update.message.chat_id)
        context.bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def dci(update: Update, context: CallbackContext):
    args = update.message.text.split(" ")
    if len(args) == 1:
        text = strings.Dci.dci_invalid
    else:
        dci = args[1]
        try:
            if dci.isdigit() and not dci.startswith('-'):
                user = tables.User.get(tables.User.user_id == update.message.from_user.id)
                user.dci = dci
                user.save()
                text = strings.Dci.dci_set.format(dci)
            else:
                text = strings.Dci.dci_invalid
        except DoesNotExist:
            text = strings.Global.user_not_exist
    context.bot.send_message(chat_id=update.message.chat_id,
                     text=text,
                     parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def name(update: Update, context: CallbackContext):
    args = update.message.text.split(" ", 1)
    if len(args) == 1:
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=strings.Name.name_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        name = args[1]
        try:
            user = tables.User.get(tables.User.user_id == update.message.from_user.id)
            user.name = name
            user.save()
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Name.name_set.format(name),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def arena(update: Update, context: CallbackContext):
    args = update.message.text.split(" ", 1)
    if len(args) == 1:
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=strings.Arena.arena_invalid,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        arena = args[1]
        try:
            user = tables.User.get(tables.User.user_id == update.message.from_user.id)
            user.arena = arena
            user.save()
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Arena.arena_set.format(arena),
                             parse_mode=telegram.ParseMode.MARKDOWN)
        except DoesNotExist:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=strings.Global.user_not_exist,
                             parse_mode=telegram.ParseMode.MARKDOWN)


@util.send_action(ChatAction.TYPING)
def logparser(update: Update, context: CallbackContext):
    file_id = update.message.document.file_id
    newFile = context.bot.get_file(file_id)
    filename = './temp/{}.log'.format(update.message.from_user.id)
    newFile.download(filename)
    with open(filename, "r") as file:
        for line in file:
            if "<== PlayerInventory.GetPlayerCardsV3" in line:
                json_object = line[line.index("{"):]
                player_cards = json.loads(json_object)
                # print(player_cards)
            if "<== PlayerInventory.GetPlayerInventory" in line:
                json_object = line[line.index("{"):]
                player_inventory = json.loads(json_object)
                text = strings.Log.log_result_parsing.format(date.today().strftime("%d/%m/%Y"),
                                                             player_inventory['payload']['vaultProgress'],
                                                             player_inventory['payload']['gems'],
                                                             player_inventory['payload']['gold'])
                context.bot.send_message(chat_id=update.message.chat_id,
                                         text=emojize(text, use_aliases=True),
                                         parse_mode=telegram.ParseMode.MARKDOWN,
                                         reply_to_message_id=update.message.message_id)
                break
    os.remove(filename)


@util.send_action(ChatAction.TYPING)
def help_pvt(update: Update, context: CallbackContext):
    if update.message.from_user.id in cacheable.get_admin_ids(context.bot):
        button_list = [InlineKeyboardButton("user", callback_data="help_user"),
                       InlineKeyboardButton("admin", callback_data="help_admin")]
        reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
        text = strings.Help.admin_help
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=emojize(text, use_aliases=True),
                         parse_mode=telegram.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)
    else:
        text = strings.Help.user_help
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=emojize(text, use_aliases=True),
                         parse_mode=telegram.ParseMode.MARKDOWN)


def help_cb(update: Update, context: CallbackContext):
    query = update.callback_query
    button_list = [InlineKeyboardButton("user", callback_data="help_user"),
                   InlineKeyboardButton("admin", callback_data="help_admin")]
    reply_markup = InlineKeyboardMarkup(util.build_menu(button_list, n_cols=2))
    if "help_user" in query.data:
        reply = strings.Help.user_help
        pass
    else:
        reply = strings.Help.admin_help
        pass
    try:
        context.bot.edit_message_text(text=reply, chat_id=query.message.chat_id,
                              message_id=query.message.message_id, reply_markup=reply_markup,
                              parse_mode=telegram.ParseMode.MARKDOWN)
    except telegram.error.BadRequest:
        context.bot.answer_callback_query(callback_query_id=update.callback_query.id)
