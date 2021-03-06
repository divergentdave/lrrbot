# LRRbot

LoadingReadyLive chatbot

## License

Licensed under Apache-2.0 ([LICENSE](LICENSE) or [https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)).

LRRbot contains modules that aren't licensed under Apache-2.0:

 * `lrrbot/commands/quote.py` is licensed under the MIT license.

## Setup instructions

### Linux (Ubuntu 16.10)
Things not covered: `keys.json` for `!highlight`, tokens and secrets for Patreon integration, Slack integration.

 1. These commands assume Ubuntu 16.10 and that you're using Bash as your shell. Adapt as needed.  
    ```
    sudo apt-get install git postgresql-9.5 postgresql-server-dev-9.5 python3.5-dev virtualenv build-essential
    git clone git@github.com:mrphlip/lrrbot
    cd lrrbot
    virtualenv -p python3.5 venv
    . venv/bin/activate
    pip install -r requirements.txt
    sudo -u postgres psql -c "CREATE USER \"$USER\";"
    sudo -u postgres psql -c "CREATE DATABASE lrrbot;"
    sudo -u postgres psql -c "GRANT ALL ON DATABASE lrrbot TO \"$USER\";"
    ```

 2. Write a `lrrbot.conf` file. Basic template:

    ```ini
    [lrrbot]
    username: 
    password: oauth
    channel: 

    preferred_url_scheme: http
    session_secret: 

    google_key:
    twitch_clientid:
    twitch_clientsecret:

    [apipass]

    [alembic]
    script_location = alembic
    ```

    Values to fill in:

    * `username`: The Twitch username of the bot. You can use your personal account, you don't need to create a new one for the bot.
    * `channel`: The channel the bot will join. Can be the same as `username`.
    * `session_secret`: A random string. You can generate one with the command `head -c 18 /dev/urandom | base64`
    * `google_key`: OAuth key to Google's services. Create a project on [Google Developer Console](https://console.developers.google.com/),
        enable Google Calendar API, and generate an API key under Credentials.
    * `twitch_clientid` and `twitch_clientsecret`: In your Twitch settings, under [Connections](https://www.twitch.tv/settings/connections)
        [register a new application](https://www.twitch.tv/kraken/oauth2/clients/new). Set the redirect URI to `http://localhost:5000/login`. 


 3. Write a `data.json` file. Basic template:
    ```
    {
        "responses": {}
    }
    ```

 4. Populate the database:
    ```
    alembic -c lrrbot.conf upgrade head
    ```
 5. Start LRRbot components:
   * IRC bot: `python start_bot.py`
   * Webserver: `python webserver.py`
   * (optional) Server-sent events server: `python eventserver.py`
 6. Go to `http://localhost:5000/login` and log in with the bot account (name in `username` config key) and the channel account (name in `channel` config key).
 7. Restart the bot.
