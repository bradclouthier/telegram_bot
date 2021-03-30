"""
Simple bot to repeatadly mock users
"""

import logging
import re
from uuid import uuid4
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import Update, ForceReply, Animation
from argparse import ArgumentParser

def get_args() -> ArgumentParser:
    """
    Fetches command line arguments
    """

    parser = ArgumentParser(description='Telegram mock bot')
    parser.add_argument(
        '-t',
        '--token',
        help='Telegram bot token',
        required=True
    )
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Turn on debug mode'
    )

    args = parser.parse_args()

    return args


def message_handler(update: Update, context:CallbackContext) -> None:
    """
    Traps the last message id for each user in the chat and mocks users if in list
    """

    if 'messages' not in context.chat_data.keys():
        context.chat_data['messages'] = {}

    # Track both the first name and last name
    message_id = update.message.message_id
    username = str(update.effective_user.username).lower()
    first_name = str(update.effective_user.first_name).lower()
    context.chat_data['messages'][first_name] = message_id
    if username not in('', None):
        context.chat_data['messages'][username] = message_id

    if 'users' not in context.chat_data.keys():
        context.chat_data['users'] = set()
    
    user_in_list = False
    if username in context.chat_data['users']:
        user_in_list = True
    elif first_name in context.chat_data['users']:
        user_in_list = True

    if get_bot_started(context) and user_in_list:
        update.message.reply_animation(
            animation='CgACAgQAAxkBAAM3YGEEfewX20iATx4Y0r4wGyPASPwAAo0CAAIfz5VSw4MlokquQZMeBA',
            caption='DUUUUUUR ' + str(update.message.text).upper() + ' DUUUUUR',
            reply_to_message_id=update.message.message_id
        )


def get_bot_started(context:CallbackContext) -> str:
    """
    Gets the status of the bot (ie start/stop)
    """

    if 'start' not in context.chat_data.keys():
        return False
    elif context.chat_data['start'] == 'Yes':
        return True
    else:
        return False


def start_command(update: Update, context:CallbackContext) -> None:
    """
    Starts the bot
    """

    update.message.reply_markdown_v2(
        'Starting the insult bot\. Your fault not mine\!',
        reply_to_message_id=update.message.message_id
    )
    context.chat_data['start'] = 'Yes'


def help_command(update: Update, _:CallbackContext) -> None:
    """
    Not exactly helpful
    """
    
    user = update.effective_user
    update.message.reply_markdown_v2(
        f'{user.mention_markdown_v2()} RTFM noob lmao'
    )


def stop_command(update: Update, context:CallbackContext) -> None:
    """
    Stops the bot
    """

    update.message.reply_markdown_v2(
        'Stopping the bot\. Thank god\!',
        reply_to_message_id=update.message.message_id
    )
    context.chat_data['start'] = 'No'


def add_command(update: Update, context:CallbackContext) -> None:
    """
    Adds a user to the insult list of the chat
    """

    if 'users' not in context.chat_data.keys():
        context.chat_data['users'] = set()

    user = update.message.text.partition(' ')[2]
    user = str(user).replace('@','').lower()
    context.chat_data['users'].add(user)
    update.message.reply_markdown_v2('{} has been added to the mock list'.format(user))


def remove_command(update: Update, context:CallbackContext) -> None:
    """
    Removes a user from the insult list
    """

    if 'users' not in context.chat_data.keys():
        context.chat_data['users'] = set()

    user = update.message.text.partition(' ')[2]
    user = str(user).replace('@','').lower()
    if user in context.chat_data['users']:
        context.chat_data['users'].remove(user)
    update.message.reply_markdown_v2('{} has been removed from the mock list'.format(user))


def mock_reply(update: Update, context:CallbackContext) -> None:
    """
    Replies back with a message sent
    """

    username = str(update.effective_user.username).lower()
    first_name = str(update.effective_user.first_name).lower()

    if 'users' not in context.chat_data.keys():
        context.chat_data['users'] = set()
    
    user_in_list = False
    if username in context.chat_data['users']:
        user_in_list = True
    elif first_name in context.chat_data['users']:
        user_in_list = True

    if get_bot_started(context) and user_in_list:
        update.message.reply_animation(
            animation='CgACAgQAAxkBAAM3YGEEfewX20iATx4Y0r4wGyPASPwAAo0CAAIfz5VSw4MlokquQZMeBA',
            caption='DUUUUUUR ' + str(update.message.text).upper() + ' DUUUUUR',
            reply_to_message_id=update.message.message_id
        )


def list_command(update: Update, context:CallbackContext) -> None:
    """
    Lists everybody on the mock list
    """

    if 'users' not in context.chat_data.keys() or len(context.chat_data['users']) == 0:
        message = "Nobody is in the mocklist" 
    else:
        users_str = "\n".join(context.chat_data['users'])
        message = "Here is everybody in the mock list: \n\n{}".format(users_str)

    update.message.reply_markdown_v2(message)
    


def teabag_command(update: Update, context:CallbackContext) -> None:
    """
    Sends a teabag gif to the user specified
    """

    user = update.message.text.partition(' ')[2]
    user_key = user.replace('@', '').lower()
    file_id = 'CgACAgQAAxkBAAIBPWBhNzriFQYd_P98riAw_B2upiruAAI7AgACA1CNUqdpIuXarrPeHgQ'

    update.message.reply_animation(
        animation=file_id,
        caption='{} suck my balls'.format(user),
        reply_to_message_id=context.chat_data['messages'][user_key]
    )


def roll_command(update: Update, context:CallbackContext) -> None:
    """
    DND Roll command. Or is it?
    """

    rollcommand = update.message.text.partition(' ')[2]
    pattern = re.compile(r'(\d*)d(\d+)(\+\d+)?')
    matches = pattern.match(rollcommand)

    if matches == None:
        update.message.reply_markdown_v2(
            "That's not how you roll\. RTFM",
            reply_to_message_id=update.message.message_id
        )
        return
    else:
        dice_roll = int(matches.group(2))
        
    if matches.group(1) == '':
        dice_num = 1
    else:
        dice_num = int(matches.group(1))
    
    if matches.group(3) not in('', None):
        modifier = str(matches.group(3)).replace('+','')
        modifier = int(modifier)
    else:
        modifier = 0

    roll_messages = []
    roll_result = dice_roll + modifier
    for i in range(1, (dice_num + 1)):
        roll_message = "Roll {}\: You rolled {}\. CRITICAL HIIIIIIT\!".format(i, roll_result)
        roll_messages.append(roll_message)

    update.message.reply_markdown_v2(
        "\n".join(roll_messages),
        reply_to_message_id=update.message.message_id
    )


def main() -> None:

    args = get_args()
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    updater = Updater(token=args.token, use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log_level)

    # Commands
    dispatcher.add_handler(CommandHandler('mockstart', start_command))
    dispatcher.add_handler(CommandHandler('mockhelp', help_command))
    dispatcher.add_handler(CommandHandler('mockstop', stop_command))
    dispatcher.add_handler(CommandHandler('mockadd', add_command))
    dispatcher.add_handler(CommandHandler('mockremove', remove_command))
    dispatcher.add_handler(CommandHandler('mocklist', list_command))
    dispatcher.add_handler(CommandHandler('teabag', teabag_command))
    dispatcher.add_handler(CommandHandler('roll', roll_command))

    # Message handlers
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))


    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()