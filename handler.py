import json
import logging
import os
from datetime import datetime, timedelta

import requests
import telegram

# Logging is cool! Yeah! It is :heart:
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    'statusCode': 200,
    'headers': {'Content-Type': 'application/json'},
    'body': json.dumps('ok')
}

ERROR_RESPONSE = {
    'statusCode': 400,
    'body': json.dumps('Oops, something went wrong!')
}


def stalk(user):
    """
    This function takes username as input
    and returns the profile as O/P
    """
    now = datetime.now()
    api = requests.get("https://api.github.com/users/" + user)
    res = api.json()
    count_api_url = os.environ.get('CONTRI_API')
    profile = ""
    if api.status_code == 200:
        pic = "<a href='{0}?a={1}'>&#8205;</a>".format(
            res["avatar_url"], datetime.now().isoformat())
        # The above line is hack of the year.
        profile += pic
        for data in res:
            url = data.endswith('url')
            ids = data.endswith('id')
            hireable = data.endswith('hireable')
            admin = data.endswith('admin')
            updated = data.endswith('updated_at')
            if url or ids or hireable or admin or updated:
                pass
            else:
                copy = data
                copy_res = fix_html_parsing(res[data])
                if copy == "created_at":
                    copy = "Joined"
                    copy_res = copy_res.split('T')[0]
                profile += "<b>{0}:</b> {1}\n".format(
                    str(copy.title().replace("_", " ")), str(copy_res))
                # Yeah I know that's too much of hacks
        if res['type'] == "User":
            streak, contri = streak_handler(user)
            profile += "<b>Today's Contribution:</b> {0}\n".format(contri)
            profile += "<b>Current Streak:</b> {0} days".format(streak)

    else:
        # Serious shit
        error_messages = {
            404: "User with username {0} does not exists, please check and try again".format(user),
            403: "API rate limit exceeded for IP address"
        }
        # Using Jio?
        fallback_error_message = (
            "Something went wrong, please check your internet connection \n"
            "Use stalk --help for Help"
        )
        profile = error_messages.get(api.status_code, fallback_error_message)
    return profile


def streak_handler(user):
    streak_count = 0
    count_api_url = os.environ.get('CONTRI_API')
    contri_api = requests.get(
        '{0}{1}/count'.format(count_api_url, user))
    contri_data = contri_api.json()
    d = datetime.today()
    y, m, d = "{0}".format(d.year), "{0}".format(
        d.month), "{0}".format(d.day)

    contri_today = contri_data.get('data').get(y).get(m).get(d)

    while contri_data.get('data').get(y).get(m).get(d) != 0:
        streak_count += 1
        d = datetime.today() - timedelta(days=streak_count)
        y, m, d = "{0}".format(d.year), "{0}".format(
            d.month), "{0}".format(d.day)

    return streak_count, contri_today


def fix_html_parsing(data):
    data.replace('>', '&gt;')
    data.replace('<', '&lt;')
    return data


def configure_telegram():
    """
    Configures the bot with a Telegram Token.
    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
    if not TELEGRAM_TOKEN:
        logger.error('The TELEGRAM_TOKEN must be set')
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)


def webhook(event, context):
    """
    Runs the Telegram webhook.
    """
    print(context)
    bot = configure_telegram()
    logger.info('Event: {0}'.format(event))

    if event.get('httpMethod') == 'POST' and event.get('body'):
        logger.info('Message received')
        update = telegram.Update.de_json(json.loads(event.get('body')), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        if text == '/start':
            reply = "Hello, Aashutosh Rathi here!" \
                    "\nTo start stalking, just enter username and we will fetch their profile for you.\n" \
                    "Project URL: https://github.com/aashutoshrathi/git-profiler-bot"
        else:
            reply = stalk(text)
        bot.sendMessage(chat_id=chat_id, parse_mode='HTML', text=reply)
        logger.info('Message sent')

        return OK_RESPONSE

    return ERROR_RESPONSE


def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """
    print(context)
    logger.info('Event: {}'.format(event))
    bot = configure_telegram()
    url = 'https://{}/{}/'.format(
        event.get('headers').get('Host'),
        event.get('requestContext').get('stage'),
    )
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE
