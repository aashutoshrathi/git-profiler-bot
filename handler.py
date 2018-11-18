import json
import os
import logging
import requests
import telegram


# Logging is cool!
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
    api = requests.get("https://api.github.com/users/" + user)
    res = api.json()
    profile = "[​​​​​​​​​​​]"
    if api.status_code == 200:
        pic = "({0})".format(res["avatar_url"])
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
                copy_res = res[data]
                if copy == "created_at":
                    copy = "Joined"
                    copy_res = copy_res.split('T')[0]
                profile += "*{0}*: {1}\n".format(
                    str(copy.title().replace("_", " ")), str(copy_res))
    else:
        error_messages = {
            404: "User with username {0} does not exists, please check and try again".format(user),
            403: "API rate limit exceeded for IP address"
        }
        fallback_error_message = (
            "Something went wrong, please check your internet connection \n"
            "Use stalk --help for Help"
        )
        profile = error_messages.get(api.status_code, fallback_error_message)
    return profile


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
            reply = """Hello, Aashutosh Rathi here!
                    To start stalking, just enter username and we will fetch their profile for you.
                    Project Link: https://github.com/aashutoshrathi/git-profiler-bot
                    """
        else:
            reply = stalk(text)
        bot.sendMessage(chat_id=chat_id, parse_mode='markdown', text=reply)
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
