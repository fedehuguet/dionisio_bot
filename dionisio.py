import os
import time
import re
from slackclient import SlackClient
slack_bot_token = keys.SLACK_BOT_TOKEN
# instantiate Slack client
slack_client = SlackClient(os.environ.get(slack_bot_token))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"