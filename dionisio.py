import requests
import json
import keys
import os
import time
import re
from slackclient import SlackClient
slack_bot_token = keys.SLACK_BOT_TOKEN
# instantiate Slack client
slack_client = SlackClient(slack_bot_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "Hola"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
greets = ['Hello','hello','Hi','hi','Yo','yo','Hola','hola'];
questions = ['Peda','peda','Fiesta','fiesta','Voy a hacer una fiesta','voy a hacer una fiesta'];
cotizaciones = ['Guardar','guardar'];


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"], event["channel"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text, channel):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    if matches:
        return (matches.group(1), matches.group(2).strip())	
    elif channel.startswith('D'):
        return (starterbot_id,message_text)
    else: 
    	return (None,None)

def get_cotizacion(key):
    resp = requests.get('http://api.dionisio.test/cotizacion/'+key)
    r = resp.json()    

    if r['error'] == False:
        return r['message']
    else: return r['message']

def store_cotizacion(parameters):
    parameters = parameters.split()
    if len(parameters)<6:
        return None
    payload = {'userId':1,'beer':parameters[1],'bottles':parameters[2],'costBeer':parameters[3],'costBottles':parameters[4],'people':parameters[5]}
    resp = requests.post('http://api.dionisio.test/cotizacion', data = payload)
    r = resp.json() 

    if r['error'] == False:
        return r['message']
    else: return r['message']

def handle_api(key):
    resp = requests.get('http://api.dionisio.test/party/'+key)
    r = resp.json()
    if r['error'] == False:
        return r['message']
    else: return r['message']

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    response = None
    
    # Check if greet
    salute = False
    for greet in greets:
        if command.startswith(greet):
        	salute = True
    
    # Check if question
    question = False
    for q in questions:
        if command.startswith(q):
            question = True
    #
    cotizacion = False
    for c in cotizaciones:
        if command.startswith(c):
            cotizacion = True

    if salute:
        response = handle_api('greet')
    elif question:
        response = get_cotizacion('1')
    elif cotizacion:
        response = store_cotizacion(command) 
    else: response = "No entiendo man. Intenta con *{}*.".format(EXAMPLE_COMMAND)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")