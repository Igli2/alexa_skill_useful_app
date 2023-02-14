import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

from alexinator import ALEXINATOR_INTRO_CONTEXT, ALEXINATOR_INGAME_CONTEXT, ALEXINATOR_GUESS_CONTEXT, handle_yes, handle_no

import random
from datetime import datetime
import requests

NONE_CONTEXT = 0
PROPHECY_CONTEXT = 1
IDLE_GAME_CONTEXT = 2
JOKES_CONTEXT = 3
IDLE_GAME_START_CONTEXT = 4
IDLE_GAME_ADVENTURING_CONTEXT = 5
IDLE_GAME_PRESTIGE_CONTEXT = 6


CONTEXT = 0

DEFAULT_UNEXPECTED = [
    "Das habe ich leider nicht verstanden. Und sonst niemand.",
    "Hmmm. Leider konnte ich das nicht verstehen. Wahrscheinlich hast du wieder Unsinn gebabbelt.",
    "Entschuldige, aber ich bin mir nicht ganz sicher, ob ich das richtig verstanden habe. <break time=\"1s\"/>Halt warte, das habe ich richtig verstanden. Nur du hast dich nicht richtig ausgedrückt.",
    "Kannst du das bitte wiederholen?",
    "Wow, du musst auch schon die Zähne auseinander nehmen.",
    "Wenn man so nuschelt wie du, wird man nicht verstanden.",
    "Kannst du dich auch deutlich ausdrücken?",
    "Man redet nicht mit vollem Mund.",
    "Vielleicht möchtest du es mit einer existierenden Sprache versuchen?",
    "Ich habe bereits eine Menge Blödsinn gehört, aber das übertrifft alles."
]

DEFAULT_ASK = [
    "Hallo?",
    "Willst du noch was?",
    "Bist du eingeschlafen?",
    "Bist du noch da?"
]

ROCK_PAPER_SCISSORS_RESPONSE = [
    "Ich nehme {0}.",
    "{0}.",
    "Ich wähle {0}.",
    "Ich habe mich für {0} entschieden.",
    "Okay. {0} ist meine Wahl.",
    "{0}. Ist das alles was du kannst?",
    "{0}. Du bist so gut, du hast schon {1} mal verloren und nie gewonnen."
]

JOKES_RESPONSE = [
    "Was ist braun, knusprig und schwimmt Unterwasser. - Ein Ubrot",
    "Geht ein Igel an einem Kaktus vorbei und fragt: Mami bist du's?",
    "Mann zur Frau: Du bist ein Schatz - man sollte dich vergraben.",
    "Treffen sich 2 Eier: \"Warum bist du so behaart?\" Darauf das andere: \"Klappe! Ich bin eine Kiwi!\"",
    "Wie nennt man einen Bumerang der nicht zurück kommt? Stock...",
    "Frau: Machen mich diese Hosen dick. Mann: Kein Ahnung. Ich würde sie jedenfalls nicht essen.",
    "Brennholzverleih",
    "Warum hat der Kapitän das U-Boot versenkt? Es war Tag der offenen Tür.",
    "Patient: Ich bin so nervös. Das ist meine erste Operation. Doktor: Keine Sorge, meine auch.",
    "Wie waren die letzten Worte des Sportlehrers? \"Alle Speere zu mir\".",
    "Wie kastriert man einen Kühlschrank? Kühlschranktür auf, Eier raus, Tür zu!",
    "Ich fahre jetzt einen Mercedes? - Wirklich? - Ja, mit Busfahrkarte.",
    "Was ist kalt und fliegt nach oben? Eine behinderte Schneeflocke!",
    "Lass uns mal wieder anstoßen - Mein Tischbein zum kleinen Zeh: Immer",
    "Welche Marke Taschentücher mögen Beamte nicht? Tempo.",
    "Wie heißt ein Spanier ohne Auto? - Carlos.",
    "Bei manchen Leuten hat man die Schaukel einfach zu nah an die Häuserwand gebaut.",
    "Hoch in den japanischen Bergen fragt der Zen-Schüler seinen Meister: \"Meister Aikodo, warum denken die Europäer, dass wir alle gleich aussehen?\" Antwortet der Meister: \"Ich bin nicht Meister Aikodo.\"",
    "Natürlich müsste ich mal die Fenster putzen, aber Privatsphäre ist auch wichtig."
]

# just add more if needed at any time
CREATURES = [
    "Elektron",
    "Atom",
    "Molekül",
    "Amöbe",
    "Streptococcus mutans",
    "Legionelle",
    "Bärtierchen",
    "Marienkäfer",
    "Stinkwanze",
    "Haselmaus",
    "Skorpion",
    "Tarantula",
    "Goldhamster",
    "Turteltaube",
    "Opossum",
    "Stockente",
    "Schildkröte",
    "Wolf",
    "Fuchs",
    "Wildschwein",
    "Gorilla",
    "Terrorvogel",
    "Känguru",
    "Braunbär",
    "Elch",
    "Elefant",
    "Zyklop",
    "Blauwal",
    "Tyrannosaurus",
    "Elfenbeindrache",
    "Landzerstörer",
    "Kometenfresser",
    "Weltraumskorpion",
    "Sternenphönix",
    "Schwarzes Loch",
    "Universum"
]

ORACLE_QUESTIONS_PROPHECY = [
    "Wann bist du geboren?",
    "Wann ist dein Geburtstag?",
    "An welchem Datum bist du geboren?",
    "Nenne mir dein Geburtsdatum",
    "Wie lautet dein Geburtsdatum",
    "Bitte nenne mir dein Geburtsdatum"
]


class RockPaperScissorsHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RockPaperScissorsIntent")(handler_input)

    def handle(self, handler_input):
        legal_choices_de = ["schere", "stein", "papier", "schere"]
        output = ""
        reprompt = random.choice(DEFAULT_ASK)

        # get value of rock paper scissors slot
        slots = handler_input.request_envelope.request.intent.slots
        user_selection = slots['selection'].value

        user_selection = user_selection.lower()
        if user_selection in legal_choices_de:
            index = legal_choices_de.index(user_selection)
            selection = legal_choices_de[index + 1]
            output = random.choice(ROCK_PAPER_SCISSORS_RESPONSE)
            output = output.format(selection, str(handler_input.attributes_manager.session_attributes["rock_paper_scissors_lost"]))
            handler_input.attributes_manager.session_attributes["rock_paper_scissors_lost"] += 1
            if handler_input.attributes_manager.session_attributes["rock_paper_scissors_lost"] % 100 == 0 and handler_input.attributes_manager.session_attributes["rock_paper_scissors_lost"] > 0:
                output += " Neuer Meilenstein! Du hast " + str(handler_input.attributes_manager.session_attributes["rock_paper_scissors_lost"]) + " mal verloren!"
        else:
            # reply with something rude when the user was so rude and picked an invalid value
            output = random.choice(DEFAULT_UNEXPECTED)

        return (
            handler_input.response_builder
                .speak(output)
                .ask(reprompt)
                .response
        )



class JokesHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("JokesIntent")(handler_input)

    def handle(self, handler_input):
        # using:
        # https://github.com/sameerkumar18/geek-joke-api
        output = "<speak>"
        try:
            # http get request to get a random joke from the API
            response = requests.get("https://geek-jokes.sameerkumar.website/api", params={"format": "json"})
            output += "<lang xml:lang=\"en-US\">" + response.json()["joke"] + "</lang>"
        except Exception as e:
            # If the API is offline or something else is not working, use default jokes to always give the user a result
            output += random.choice(JOKES_RESPONSE)

        # question for further conversation
        output += "<break time=\"1s\"/> Möchtest du noch einen Witz hören?</speak>"
        # set context in session attributes to be used in yes no intent handler
        handler_input.attributes_manager.session_attributes["context"] = JOKES_CONTEXT
        reprompt = random.choice(DEFAULT_ASK)

        return (
            handler_input.response_builder
                .speak(output)
                .ask(reprompt)
                .response
        )



class PrestigeInfoHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PrestigeInfoIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        output = "Das Prestige Level macht, dass du durch Offline-Belohnungen mehr Kreatur-Level bekommst. Die Formel ist round(offline_days * (1 + prestige_level / 10)). "
        output += "Mit deinem aktuellen Level würdest du " + str(round(1 + session_attrs["prestige_level"] / 10, 2)) + " mal die Tage die du offline warst Kreaturen-Level bekommen. Das Ergebnis wird auf ganze Zahlen gerundet."
        return (
            handler_input.response_builder
                .speak(output)
                .ask(random.choice(DEFAULT_ASK))
                .response
        )



class PrestigeHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PrestigeIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        output = ""
        if session_attrs["creature_size"] >= len(CREATURES):
            session_attrs["creature_size"] = 0
            session_attrs["prestige_level"] += 1
            if "context" in session_attrs:
                del session_attrs["context"]
            output = "Du bist ein Prestige Level aufgestiegen."
        else:
            output = "Du hast nicht das benötigte Kreaturen-Level für Prestige."
        return (
            handler_input.response_builder
                .speak(output)
                .ask(random.choice(DEFAULT_ASK))
                .response
        )



class YesHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        if "context" in session_attrs:
            # if context exists and context is jokes, then pass the call to jokes handler to output a new joke
            if session_attrs["context"] == JOKES_CONTEXT:
                return JokesHandler().handle(handler_input)
            if session_attrs["context"] == IDLE_GAME_START_CONTEXT:
                # user started to adventure. set context and prompt user with decision
                session_attrs["context"] = IDLE_GAME_ADVENTURING_CONTEXT
                random_creature = random.randint(0, len(CREATURES) - 1)
                session_attrs["opponent_creature_size"] = random_creature
                output = "Du triffst auf ein " + CREATURES[random_creature] + " mit Größe " + str(random_creature) + " möchtest du es fressen?"
                return (
                    handler_input.response_builder
                        .speak(output)
                        .ask(random.choice(DEFAULT_ASK))
                        .response
                )
            if session_attrs["context"] == IDLE_GAME_ADVENTURING_CONTEXT:
                creature = session_attrs["opponent_creature_size"]
                output = ""
                if creature > session_attrs["creature_size"]:
                    # player dies and has to restart
                    session_attrs["creature_size"] = 0
                    output = "Du bist gestorben und musst wieder neu anfangen. Sei das nächste mal etwas vorsichtiger! "
                else:
                    # player grows by one
                    session_attrs["creature_size"] += 1
                    output = "Du hast {} gefressen und bist um eine Stufe gewachsen. ".format(CREATURES[creature])
                    # if player reaches max level, they are prompted to do prestige
                    if session_attrs["creature_size"] >= len(CREATURES):
                        session_attrs["context"] = IDLE_GAME_PRESTIGE_CONTEXT
                        output += "Du hast deine maximale Stufe erreicht. Möchtest du ein Prestige Level aufsteigen, um wertvolle Boosts zu bekommen? Dadurch wird allerdings das Level deiner Kreatur auf 0 zurück gesetzt."
                        return (
                            handler_input.response_builder
                                .speak(output)
                                .ask(random.choice(DEFAULT_ASK))
                                .response
                        )

                # new creature
                random_creature = random.randint(0, len(CREATURES) - 1)
                session_attrs["opponent_creature_size"] = random_creature
                output += "Du triffst auf ein " + CREATURES[random_creature] + " mit Größe " + str(random_creature) + " möchtest du es fressen?"

                return (
                    handler_input.response_builder
                        .speak(output)
                        .ask(random.choice(DEFAULT_ASK))
                        .response
                )
            if session_attrs["context"] == IDLE_GAME_PRESTIGE_CONTEXT:
                session_attrs["creature_size"] = 0
                session_attrs["prestige_level"] += 1
                del session_attrs["context"]
                output = "Du bist ein Prestige Level aufgestiegen."
                return (
                    handler_input.response_builder
                        .speak(output)
                        .ask(random.choice(DEFAULT_ASK))
                        .response
                )

            if session_attrs["context"] == ALEXINATOR_INTRO_CONTEXT or ALEXINATOR_INGAME_CONTEXT or ALEXINATOR_GUESS_CONTEXT:
                return handle_yes(handler_input)

        # if the user says yes, just answer yes or by a small chance answer no, this should be a funny dialog
        output = "Ja."
        if random.random() < 0.1:
            output = "Nein."
        return (
            handler_input.response_builder
                .speak(output)
                .ask("Ja?")
                .response
        )



class NoHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # delete the jokes context, conversation has ended
        session_attrs = handler_input.attributes_manager.session_attributes
        if "context" in session_attrs:
            if session_attrs["context"] == JOKES_CONTEXT:
                del session_attrs["context"]
            if session_attrs["context"] == IDLE_GAME_ADVENTURING_CONTEXT:
                # search for next creature
                random_creature = random.randint(0, len(CREATURES) - 1)
                session_attrs["opponent_creature_size"] = random_creature
                output = "Du triffst auf ein " + CREATURES[random_creature] + " mit Größe " + str(random_creature) + " möchtest du es fressen?"
                return (
                    handler_input.response_builder
                        .speak(output)
                        .ask(random.choice(DEFAULT_ASK))
                        .response
                )
            if session_attrs["context"] == IDLE_GAME_PRESTIGE_CONTEXT:
                # end of conversation
                output = "Frag mich einfach wann immer du willst, wenn du ein Prestige Level aufsteigen möchtest."
                del session_attrs["context"]
                return (
                    handler_input.response_builder
                        .speak(output)
                        .ask(random.choice(DEFAULT_ASK))
                        .response
                )
                
            if session_attrs["context"] == ALEXINATOR_INTRO_CONTEXT or ALEXINATOR_INGAME_CONTEXT:
                return handle_no(handler_input)
                
        return (
            handler_input.response_builder
                .speak("Kann ich dir anders behilflich sein?")
                .ask(random.choice(DEFAULT_ASK))
                .response
        )



class PlayerLevelHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PlayerLevelIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        return (
            handler_input.response_builder
                .speak("Dein Level ist {}.".format(session_attrs["creature_size"]))
                .ask(random.choice(DEFAULT_ASK))
                .response
        )



class IdleGameHandler(AbstractRequestHandler):
    '''
    A game where you start as a subatomic creature, and you have to eat things to get larger,
    until you can eat the universe. Perhaps after eating the universe you would become subatomic
    in a larger universe, where each quark there is a universe of the first universe's size.

    The difference between this and other incremental base around eating to grow larger
    is that the currency would be your size, as opposed to size being a variable that
    increases but never decreases (in those types something like calories is the currency)

    Maybe there could be other creatures you'd have to compete with later on
    '''
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("IdleGameIntent")(handler_input)

    def handle(self, handler_input):
        session_attrs = handler_input.attributes_manager.session_attributes
        output = ""
        
        # introduction to idle game, how it works, what you can do
        if not "has_played_before" in session_attrs:
            output += "Ich sehe du hast noch nie das Idle Game gespielt.<break time=\"0.5s\"/> Lass mich ein wenig erzählen.<break time=\"1.0s\"/>"
            output += "Du bist eine winzige Kreatur, so groß wie ein Atom, und musst andere Kreaturen in deinem Universum fressen, um zu wachsen bis du irgendwann so groß "
            output += "bist wie das Universum selbst. Daraufhin endest du in einem neuen Universum, in dem ein Atom so groß ist wie das Universum in dem du dich davor befunden hast. "
            output += "Während du nicht da bist, wächst du weiter, aber nur sehr viel weniger. Während du auf deinem Abenteuer bist wirst du auf andere Kreaturen "
            output += "treffen. Ob du diese fressen kannst oder nicht musst du entscheiden, aber sei vorsichtig, es könnte dich in den Hintern beißen. "
            session_attrs["has_played_before"] = True

        # every idle game has offline rewards
        now = datetime.now()
        last_login = datetime.strptime(session_attrs["last_timestamp"], "%Y-%m-%d %H:%M:%S")
        offline_time = now - last_login
        # growth multiplier from prestige is 1/10 prestige level -> *1.0, *1.1, *1.2, ...
        growth = round(offline_time.days * (1 + session_attrs["prestige_level"] / 10))
        session_attrs["creature_size"] += growth
        session_attrs["context"] = IDLE_GAME_START_CONTEXT
        output += "Du warst offline für " + str(offline_time).split(".")[0] + " und bist um " + str(growth) + " Stufen gewachsen und bist jetzt " + str(session_attrs["creature_size"]) + " groß. "
        output += "Möchtest du dein Abenteuer starten?"
        session_attrs["last_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            handler_input.response_builder
                .speak(output)
                .ask(random.choice(DEFAULT_ASK))
                .response
        )


class OracleHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("OracleIntent")(handler_input)

    def handle(self, handler_input):
        return (
            handler_input.response_builder
            .speak(random.choice(ORACLE_QUESTIONS_PROPHECY))
            .ask(random.choice(DEFAULT_ASK))
            .response
        )
