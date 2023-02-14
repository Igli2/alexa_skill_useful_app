# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.

# dynamo db reference
# https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-session-persistence.html

import logging
import ask_sdk_core.utils as ask_utils

# imports for dynamo db
import os
import traceback
import boto3
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from custom_handlers import RockPaperScissorsHandler, JokesHandler, IdleGameHandler, OracleHandler, YesHandler, NoHandler, PlayerLevelHandler, PrestigeInfoHandler, PrestigeHandler
from alexinator import Alexinator, AlexinatorIntentHandler

from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# initialize dynamo db adapter
ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')

ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)



# load and save persistent attributes
def load_resources(handler_input):
    attr = handler_input.attributes_manager.persistent_attributes
    if not attr:
        attr["last_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attr["login_count"] = 0
        attr["rock_paper_scissors_lost"] = 0
        attr["creature_size"] = 0
        attr["has_played_before"] = False
        attr["prestige_level"] = 0
    
    handler_input.attributes_manager.session_attributes = attr

def save_resources(handler_input):
    session_attr = handler_input.attributes_manager.session_attributes

    session_attr["last_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_attr["login_count"] += 1
    # remove context as this should never be saved in the database and is only used per session
    if "context" in session_attr:
        del session_attr["context"]
    if "opponent_creature_size" in session_attr:
        del session_attr["opponent_creature_size"]

    handler_input.attributes_manager.persistent_attributes = session_attr
    handler_input.attributes_manager.save_persistent_attributes()



'''BuiltIn Handlers'''
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        load_resources(handler_input)

        speak_output = "Willkommen bei der Useful App mit vielen tollen Features."

        # introduction if user has never started the skill before
        if handler_input.attributes_manager.session_attributes["login_count"] == 0:
            speak_output += " Ich sehe du hast noch nie diesen Skill verwendet. Aber das ist kein Problem."
            speak_output += " Hier ist ein kleiner Überblick, was du alles machen kannst: Schere Stein Papier, lustige Witze und ein kleines Idle Game."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Du kannst das Idle Game spielen, nach lustigen Witzen fragen oder Schere Stein Papier spielen."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Bis bald!"
        save_resources(handler_input)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Was möchtest du nochmal? (Fallback Intent Handler)"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "Intent Reflector Handler " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Ein Fehler ist aufgetreten. Da hat wohl jemand schlechten Code geschrieben."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


# sb = SkillBuilder()
# dynamo db skill builder
sb = CustomSkillBuilder(persistence_adapter = dynamodb_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RockPaperScissorsHandler())
sb.add_request_handler(JokesHandler())
sb.add_request_handler(OracleHandler())
sb.add_request_handler(IdleGameHandler())
sb.add_request_handler(YesHandler())
sb.add_request_handler(NoHandler())
sb.add_request_handler(PlayerLevelHandler())
sb.add_request_handler(PrestigeInfoHandler())
sb.add_request_handler(PrestigeHandler())
sb.add_request_handler(AlexinatorIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()