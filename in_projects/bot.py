import datetime
import math

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

STATE = None

BIRTH_YEAR = 1
BIRTH_MONTH = 2
BIRTH_DAY = 3

def hello(update, context):
    update.message.reply_text(f'Hello {update.effective_user.first_name}')
    update.message.reply_text(f'https://python-telegram-bot.readthedocs.io/en/stable/telegram.game.html')


def start(update, context):
    first_name = update.message.chat.first_name
    update.message.reply_text(f"Hi {first_name}, nice to meet you!")

# function to handle the /help command
def help(update, context):
   update.message.reply_text('help command received, how can i help u ?')

# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text('an error occured')

# function to handle normal text
def text(update, context):
    global STATE

    if STATE == BIRTH_YEAR:
        return received_birth_year(update, context)

    if STATE == BIRTH_MONTH:
        return received_birth_month(update, context)

    if STATE == BIRTH_DAY:
        return received_birth_day(update, context)


def biorhythm(update, context):
    print("ok")
    start_getting_birthday_info(update, context)


def biorhythm_out(update, context):
    user_biorhythm = calculate_biorhythm(
        context.user_data['birthday'])

    update.message.reply_text(f"Phisical: {user_biorhythm['phisical']}")
    update.message.reply_text(f"Emotional: {user_biorhythm['emotional']}")
    update.message.reply_text(f"Intellectual: {user_biorhythm['intellectual']}")


def start_getting_birthday_info(update, context):
    global STATE
    STATE = BIRTH_YEAR
    update.message.reply_text(f"I would need to know your birthday, so tell me what year did you born in...")


def received_birth_year(update, context):
    global STATE

    try:
        today = datetime.date.today()
        year = int(update.message.text)

        if year > today.year:
            raise ValueError("invalid value")

        context.user_data['birth_year'] = year
        update.message.reply_text(f"ok, now I need to know the month (in numerical form)...")
        STATE = BIRTH_MONTH
    except:
        update.message.reply_text("it's funny but it doesn't seem to be correct...")


def received_birth_month(update, context):
    global STATE

    try:
        today = datetime.date.today()
        month = int(update.message.text)

        if month > 12 or month < 1:
            raise ValueError("invalid value")

        context.user_data['birth_month'] = month
        update.message.reply_text(f"great! And now, the day...")
        STATE = BIRTH_DAY
    except:
        update.message.reply_text("it's funny but it doesn't seem to be correct...")


def received_birth_day(update, context):
    global STATE

    try:
        today = datetime.date.today()
        dd = int(update.message.text)
        yyyy = context.user_data['birth_year']
        mm = context.user_data['birth_month']
        birthday = datetime.date(year=yyyy, month=mm, day=dd)

        if today - birthday < datetime.timedelta(days=0):
            raise ValueError("invalid value")

        context.user_data['birthday'] = birthday
        STATE = None
        update.message.reply_text(f'ok, you born on {birthday}, this is u biorhythm')
        biorhythm_out(update, context)
    except:
        update.message.reply_text("it's funny but it doesn't seem to be correct...")


def calculate_biorhythm(birthdate):
    today = datetime.date.today()
    delta = today - birthdate
    days = delta.days

    phisical = math.sin(2*math.pi*(days/23))
    emotional = math.sin(2*math.pi*(days/28))
    intellectual = math.sin(2*math.pi*(days/33))

    biorhythm = {}
    biorhythm['phisical'] = int(phisical * 10000)/100
    biorhythm['emotional'] = int(emotional * 10000)/100
    biorhythm['intellectual'] = int(intellectual * 10000)/100

    biorhythm['phisical_critical_day'] = (phisical == 0)
    biorhythm['emotional_critical_day'] = (emotional == 0)
    biorhythm['intellectual_critical_day'] = (intellectual == 0)

    return biorhythm


def photo(update, context):
    update.message.reply_text("its, doesnt work right now!")


def main():
   # TOKEN = "5029290279:AAGjn54yO1PgY9aWsGAPuk_U7hC0WCGkSL4"

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # add handlers for start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("biorhythm", biorhythm))
    dispatcher.add_handler(CommandHandler('hello', hello))
    # add an handler for normal text (not commands)
    dispatcher.add_handler(MessageHandler(Filters.text, text))
    # add an handler for errors
    dispatcher.add_error_handler(error)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()