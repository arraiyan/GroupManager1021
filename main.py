
import logging
import time
from telegram import *
from telegram.ext import *
from inf import env
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    return


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(env.HelpText)
    return


def check_admin(update: Update, context: CallbackContext) -> None:
    is_admin = False
    CurrentMemberData = context.bot.get_chat_member(
        chat_id=update.message.chat_id, user_id=update.message.from_user.id).to_dict()
    print(CurrentMemberData)
    if (CurrentMemberData['status'] == 'creator') or (CurrentMemberData['status'] == 'administrator'):
        is_admin = True
    else:
        is_admin = False
    return is_admin


def new_join(update: Update, context: CallbackContext) -> None:
    user = update.message.new_chat_members[0]
    name = user.username
    fname = str(user.first_name)+str(' ')+str(user.last_name)
    txt = f'@{name}\n\nHi {fname} \n' + env.WelComeText
    context.bot.send_message(
        chat_id=update.message.chat_id, text=txt, parse_mode='HTML')
    print(name)
    return


def spam(text, update, context):
    result = False
    if check_admin(update, context) == False:
        mod = str(text).lower().replace(' ', '')
        for i in env.restricted_words:
            if i in mod:
                return True
        return result
    else:
        return


def echo(update: Update, context: CallbackContext) -> None:
    txt = update.message.text
    txthtm = update.message.text_html
    if not update.message.chat.type == 'private':
        if spam(txthtm, update, context):
            
            un = update.message.from_user.username
            fn = update.message.from_user.first_name + ' ' + update.message.from_user.last_name #fn refers to full name 
            d = update.message.reply_text(
                f'⚠️Warning: {un}\n{fn} Don\'t post spam links!\n')
            time.sleep(8)
            context.bot.delete_message(
                chat_id=update.message.chat_id, message_id=update.message.message_id)
            time.sleep(2)
            context.bot.delete_message(
                chat_id=update.message.chat_id, message_id=d.message_id)

            pass
        return
    return


def ban(update: Update, context: CallbackContext) -> None:
    if check_admin(update, context):
        try:

            u = update.message.reply_to_message
            un = u.from_user.username
            fn = u.from_user.first_name + ' ' + u.from_user.last_name
            update.message.reply_text(
                f'⚠️Warning: @{un}\n{fn} you have been restricted!\n Cause you have posted Spam links in our telegram group')
            user = update.message.reply_to_message.from_user.id
            context.bot.ban_chat_member(chat_id=u.chat_id, user_id=user)
            context.bot.delete_message(
                chat_id=u.chat_id, message_id=u.message_id)
            return
        except:
            return
    else:
        return


def main() -> None:
    updater = Updater(env.API_KEY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("ban", ban))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, new_join))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
