import requests
import json
import keys
import time
import re
from slackclient import SlackClient
from rasa_nlu.converters import load_data
from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Trainer
from rasa_nlu.model import Metadata, Interpreter

slack_bot_token = keys.SLACK_BOT_TOKEN
# instantiate Slack client
slack_client = SlackClient(slack_bot_token)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "Hi there"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

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
        return (matches.group(1), message_text)	
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

def handle_salute(key):
    resp = requests.get('http://api.dionisio.test/party/'+key)
    r = resp.json()
    if r['error'] == False:
        return r['message']
    else: return r['message']

def handle_command(interpreter, command, channel):
    """
        Executes bot command if the command is known
    """
    response = None
    
    parsed_message = interpreter.parse(command)
    print parsed_message

    # Check intent
    if parsed_message['intent']['name'] == "greeting":
       response = handle_salute('greeting')
    elif parsed_message['intent']['name'] == "goodbye":
       response = handle_salute('goodbye')
    else: response = "Sorry I could not understand, try with *{}*.".format(EXAMPLE_COMMAND)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
    
    #NLU Rasa implementation
    print("Starting training")
    
    training_data = load_data('data/demo_dionisio.json')
    print("Data loaded")
    
    trainer = Trainer(RasaNLUConfig("configs/config_spacy.json"))
    print("Trainer instantiated")
    
    trainer.train(training_data)
    print("Trainer trained")
    
    model_directory = trainer.persist('./models')
    print("Persistence finished")

    print("Instantiating interpreter...")
    interpreter = Interpreter.load(model_directory, RasaNLUConfig("configs/config_spacy.json"))
    print("Finished")
    #interpreter = Interpreter.load('./models/default/model_20180316-163725', RasaNLUConfig("configs/config_spacy.json"))
    
    if slack_client.rtm_connect(with_team_state=False):
        print("Chat bot running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(interpreter, command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")