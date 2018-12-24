# git-profiler-bot
[![Build Status](https://travis-ci.org/aashutoshrathi/git-profiler-bot.png)](https://travis-ci.org/aashutoshrathi/git-profiler-bot)

This is a Telegram bot which fetches Profile summary using GitHub API.
Ported to serverless as part of #noserverNovember

## How to use 🤔

- Visit [Git Profile Bot](http://t.me/git_profile_bot)
- Start chatting.

## Usage

### What do I need 🤔

- A AWS key configured locally, see [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/).
- NodeJS.
- A Telegram account.

### Installing

```sh
# Install the Serverless Framework
$ npm install serverless -g

# Install the necessary plugins
$ npm install

# Get a bot from Telegram, sending this message to @BotFather
Go to https://t.me/BotFather
$ /newbot

# Put the token received into a file called serverless.env.yml, like this
$ cat >serverless.env.yml
TELEGRAM_TOKEN: <your_token>

# Change app and tenant to your ones
$ nano serverless.yml
app: <your-app>
tenant: <username>

# Export you AWS Keys to your shell

- Get some help from [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/)

# Deploy it!
$ serverless deploy

# With the URL returned in the output, configure the Webhook
$ curl -X POST https://<your_url>.amazonaws.com/dev/set_webhook
```

### Testing

```sh
# Create a virtual python env
$ python3 -m venv pytest-env

# Activate the virtual env
$ source pytest-env/bin/activate

# Install following modules
$ pip3 install -r requirements.txt

# Run tests
$ pytest
```

## Contributing

Feel free to raise issues and send PRs. :smile:

---

<p align="center"> Made with ❤️ by <a href="https://github.com/aashutoshrathi">Aashutosh Rathi</a></p>
