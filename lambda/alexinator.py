import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler

from utils import update_session_attributes, get_session_attribute

import random

ALEXINATOR_INTRO_CONTEXT = 7
ALEXINATOR_INGAME_CONTEXT = 8
ALEXINATOR_GUESS_CONTEXT = 9
ALEXINATOR_RETRY_CONTEXT = 10

database = {
    "details": ["Das habe ich mir tatsächlich gedacht.", "Das habe ich mir bereits gedacht.",
                "Jetzt geht mir ein Licht auf.", "Ich habe mit nichts Anderem gerechnet.",
                "Das vereinfacht die Suche natürlich.", "So habe ich mir das vorgestellt."],
    "persons": [
        {
            "name": "Iron Man",
            "human": True,
            "physicist": True,
            "usa": True,
            "inventor": True,
            "movie": True,
            "male": True,
            "game": True,
            "land": True,
            "talk": True,
            "famous": True,
            "scientist": True,
            "mechanic": True,
            "artist": False,
            "fish": False,
            "president": False,
            "original": False,
            "singer": False,
            "nobel prize": False,
            "musician": False,
            "sculptor": False,
            "ocean": False,
            "switzerland": False
        },
        {
            "name": "Albert Einstein",
            "human": True,
            "original": True,
            "inventor": True,
            "physicist": True,
            "switzerland": True,
            "usa": True,
            "nobel prize": True,
            "male": True,
            "land": True,
            "talk": True,
            "famous": True,
            "game": False,
            "artist": False,
            "scientist": False,
            "movie": False,
            "fish": False,
            "president": False,
            "singer": False,
            "musician": False,
            "mechanic": False,
            "sculptor": False,
            "ocean": False
        },
        {
            "name": "Nemo",
            "fish": True,
            "movie": True,
            "male": True,
            "ocean": True,
            "talk": True,
            "human": False,
            "game": False,
            "artist": False,
            "scientist": False,
            "physicist": False,
            "president": False,
            "original": False,
            "singer": False,
            "inventor": False,
            "nobel prize": False,
            "land": False,
            "famous": False,
            "musician": False,
            "mechanic": False,
            "usa": False,
            "sculptor": False,
            "switzerland": False
        },
        {
            "name": "Barack Obama",
            "usa": True,
            "president": True,
            "original": True,
            "nobel prize": True,
            "male": True,
            "land": True,
            "talk": True,
            "famous": True,
            "human": False,
            "game": False,
            "artist": False,
            "scientist": False,
            "physicist": False,
            "movie": False,
            "fish": False,
            "singer": False,
            "inventor": False,
            "musician": False,
            "mechanic": False,
            "sculptor": False,
            "ocean": False,
            "switzerland": False
        },
        {
            "name": "Michael Jackson",
            "famous": True,
            "male": True,
            "singer": True,
            "usa": True,
            "land": True,
            "musician": True,
            "human": False,
            "game": False,
            "artist": False,
            "scientist": False,
            "physicist": False,
            "movie": False,
            "talk": False,
            "fish": False,
            "president": False,
            "original": False,
            "inventor": False,
            "nobel prize": False,
            "mechanic": False,
            "sculptor": False,
            "ocean": False,
            "switzerland": False
        },
        {
            "name": "Leonardo da Vinci",
            "famous": True,
            "male": True,
            "artist": True,
            "inventor": True,
            "musician": True,
            "scientist": True,
            "mechanic": True,
            "sculptor": True,
            "land": True,
            "human": False,
            "game": False,
            "physicist": False,
            "movie": False,
            "talk": False,
            "fish": False,
            "president": False,
            "original": False,
            "singer": False,
            "nobel prize": False,
            "usa": False,
            "ocean": False,
            "switzerland": False
        }
    ],
    "questions": [
        {
            "questions": [
                "Ist deine Figur ein Physiker?",
                "Ist dein Charakter ein Physiker?"
            ],
            "property": "physicist"
        },
        {
            "questions": [
                "Ist deine Figur US-Amerikaner?",
                "Stammt deine Figur aus den USA?",
                "Wohnt oder lebte deine Figur in den USA?"
            ],
            "property": "usa"
        },
        {
            "questions": [
                "Ist deine Figur ein Erfinder?",
                "Ist deine Figur fuer Erfindungen bekannt?"
            ],
            "property": "inventor"
        },
        {
            "questions": [
                "Kennt man deine Figur aus Filmen?",
                "Spielt deine Figur eine Rolle in einem Film?"
            ],
            "property": "movie"
        },
        {
            "questions": [
                "Ist deine Figur maennlich?"
            ],
            "property": "male"
        },
        {
            "questions": [
                "Spielt deine Figur in einem Spiel mit?",
                "Kennt man deine Figur aus einem Spiel?"
            ],
            "property": "game"
        },
        {
            "questions": [
                "Lebt deine Figur ueber Wasser?"
            ],
            "property": "land"
        },
        {
            "questions": [
                "Kann deine Figur sprechen?"
            ],
            "property": "talk"
        },
        {
            "questions": [
                "Ist deine Figur beruehmt?",
                "Ist deine Figur aussergewoehnlich bekannt?"
            ],
            "property": "famous"
        },
        {
            "questions": [
                "Ist deine Figur menschlich?",
                "Ist deine Figur ein Mensch?"
            ],
            "property": "human"
        },
        {
            "questions": [
                "Ist deine Figur eine reelle Person?",
                "Existiert deine Figur reell?"
            ],
            "property": "original"
        },
        {
            "questions": [
                "Ist deine Figur aus der Schweiz?"
            ],
            "property": "switzerland"
        },
        {
            "questions": [
                "Hat deine Figur einen Nobelpreis gewonnen?",
                "Hat deine Figur den Nobelpreis erworben?"
            ],
            "property": "nobel prize"
        },
        {
            "questions": [
                "Ist deine Figur ein Fisch?"
            ],
            "property": "fish"
        },
        {
            "questions": [
                "Lebt deine Figur unter Wasser?",
                "Lebt deine Figur im Ozean?"
            ],
            "property": "ocean"
        },
        {
            "questions": [
                "Hat deine Figur das Amt des Praesidenten eingenommen?",
                "Ist deine Figur Praesident?"
            ],
            "property": "president"
        },
        {
            "questions": [
                "Ist deine Figur Saenger?"
            ],
            "property": "singer"
        },
        {
            "questions": [
                "Ist deine Figur Kuenstler?",
                "Ist deine Figur Maler?"
            ],
            "property": "artist"
        },
        {
            "questions": [
                "Ist deine Figur Musiker?"
            ],
            "property": "musician"
        },
        {
            "questions": [
                "Ist deine Figur Naturwissenschaftler?",
                "Ist deine Figur Wissenschaftler?"
            ],
            "property": "scientist"
        },
        {
            "questions": [
                "Ist deine Figur Mechaniker?"
            ],
            "property": "mechanic"
        },
        {
            "questions": [
                "Ist deine Figur Bildhauer?",
                "Ist deine Figur Steinmetz?"
            ],
            "property": "sculptor"
        }
    ]
}

intro = [
    "Denke nun an eine der genannten Figuren. Ich werde versuchen, sie zu erraten.",
    "Hast du eine der Figuren im Kopf? Denn ich fange nun an zu fragen.",
    "Nun solltest du deine Figur im Kopf haben. Ich werde nun herausfinden, welche Figur du gewählt hast."
]

wrong_guess = [
    "Das habe ich nicht erwartet.", "Ich war mir so sicher.", "Das glaube ich jetzt nicht.", "Lass es mich weiterhin versuchen.", "Ich bin der Antwort ganz nah."
]

correct_guess = [
    "Ich wusste es!", "Ich habe dich durchschaut!", "Das war doch von Anfang an klar.", "Du kannst es ruhig etwas schwerer machen.", "Nächstes Mal bitte eine weniger leicht zu erratende Figur."
]

retry_output = [
    "Möchtest du es nochmal versuchen?", "Möchtest du es noch einmal versuchen?", "Willst du es noch einmal versuchen?", "Willst du es nochmal versuchen?", "Gehen wir in die nächste Runde?", "Noch einmal?"
]

class Alexinator:
    def __init__(self, database=None, context=None):
        if database is not None:
            self.persons: List = database["persons"]
            self.questions: List = database["questions"]
            self.details: List = database["details"]
            self.asked = None
            self.matches = self.persons.copy()
            self.known_properties = []
        elif context is not None:
            self.matches = context["matches"]
            self.questions = context["questions"]
            self.details = context["details"]
            self.asked = context["asked"]
            self.known_properties = context["known_properties"]

    def reset(self):
        self.matches = self.persons.copy()
        self.known_properties = []

    def make_question(self):
        question = random.choice(self.questions)
        while question["property"] in self.known_properties:
            question = random.choice(self.questions)
        self.asked = question["property"]
        return random.choice(question["questions"])

    def receive_answer(self, property: str, value: bool):
        self.known_properties.append(property)
        to_remove = []
        for person in self.matches:
            if property in person:
                if person[property] != value:
                    to_remove.append(person)

        for person in to_remove:
            self.matches.remove(person)

    def pop_mismatch(self):
        self.matches.pop(0)

    def knows_person(self):
        return len(self.matches) == 1

    def get_match(self):
        return self.matches[0]
        
    def is_list_empty(self):
        return len(self.matches) == 0


class AlexinatorIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AlexinatorIntent")(handler_input)

    def handle(self, handler_input):
        alexinator = create_alexinator(handler_input, True)
        store_alexinator(alexinator, handler_input)

        speak_output = f"Ich bin der Alexinator. Derzeit kenne ich {len(alexinator.persons)} Persönlichkeiten und {len(alexinator.questions)} Eigenschaften.<break time=\"0.5s\"/>Wähle zwischen folgenden Persönlichkeiten:"
        for i in range(len(alexinator.matches) - 1):
            speak_output += f" {alexinator.matches[i]['name']},"
        speak_output += f" und {alexinator.matches[len(alexinator.matches) - 1]['name']}. "
        speak_output += random.choice(intro)
        speak_output += " Hast du soweit alles verstanden?"

        update_session_attributes(handler_input, "context", ALEXINATOR_INTRO_CONTEXT)
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


def reset_alexinator(handler_input):
    store_alexinator(create_alexinator(handler_input, True), handler_input)

def create_alexinator(handler_input, force_reset=False):
    value = get_session_attribute(handler_input, "alexinator_context")
    if value is None or force_reset:
        return Alexinator(database=database)
    else:
        return Alexinator(context=value)


def store_alexinator(alexinator: Alexinator, handler_input):
    context = {
        "matches": alexinator.matches,
        "questions": alexinator.questions,
        "details": alexinator.details,
        "known_properties": alexinator.known_properties,
        "asked": alexinator.asked
    }
    update_session_attributes(handler_input, "alexinator_context", context)

def make_question(handler_input, prefix_output=""):
    alexinator = create_alexinator(handler_input)
    question = alexinator.make_question()
    store_alexinator(alexinator, handler_input)
    return (
        handler_input.response_builder
        .speak(prefix_output + question)
        .ask("Bist du dir unsicher?")
        .response
    )

def answer_alexinator(handler_input, value: bool):
    alexinator = create_alexinator(handler_input)      
    alexinator.receive_answer(alexinator.asked, value)
    store_alexinator(alexinator, handler_input)
    if alexinator.knows_person():
        update_session_attributes(handler_input, "context", ALEXINATOR_GUESS_CONTEXT)
        return (
            handler_input.response_builder
            .speak(f"Ich weiß wen du dir ausgedacht hast. Ist es {alexinator.get_match()['name']}?")
            .ask("Hast du deine Figur vergessen?")
            .response
        )
    elif alexinator.is_list_empty():
        return no_matches(handler_input)
    else:
        return make_question(handler_input)

def guessed_wrong(handler_input):
    alexinator = create_alexinator(handler_input)
    alexinator.pop_mismatch()
    store_alexinator(alexinator, handler_input)
    if alexinator.is_list_empty():
        return no_matches(handler_input)
    else:
        return make_question(handler_input, random.choice(wrong_guess))

def no_matches(handler_input):
    reset_alexinator(handler_input)
    update_session_attributes(handler_input, "context", ALEXINATOR_RETRY_CONTEXT)
    return (
            handler_input.response_builder
            .speak("Es scheint ich kenne deine Figur nicht. Wahrscheinlich habe ich sie nie persönlich getroffen oder bereits vergessen. " + random.choice(retry_output))
            .ask("Vielleicht errate ich ja deine nächste Person.")
            .response
        )
def guessed_right(handler_input):
    reset_alexinator(handler_input)
    update_session_attributes(handler_input, "context", ALEXINATOR_RETRY_CONTEXT)
    return (
        handler_input.response_builder
        .speak(random.choice(correct_guess) + " " + random.choice(retry_output))
        .ask("Keine Angst!")
        .response
    )

def handle_yes(handler_input):
    value = get_session_attribute(handler_input, "context")
    if value == ALEXINATOR_INTRO_CONTEXT:
        update_session_attributes(handler_input, "context", ALEXINATOR_INGAME_CONTEXT)
        return make_question(handler_input)
    elif value == ALEXINATOR_INGAME_CONTEXT:
        return answer_alexinator(handler_input, True)
    elif value == ALEXINATOR_GUESS_CONTEXT:
        return guessed_right(handler_input)
    elif value == ALEXINATOR_RETRY_CONTEXT:
        update_session_attributes(handler_input, "context", ALEXINATOR_INGAME_CONTEXT)
        return make_question(handler_input, "Sehr gut. ")

def handle_no(handler_input):
    value = get_session_attribute(handler_input, "context")
    if value == ALEXINATOR_INTRO_CONTEXT:
        return AlexinatorIntentHandler().handle(handler_input)
    elif value == ALEXINATOR_INGAME_CONTEXT:
        return answer_alexinator(handler_input, False)
    elif value == ALEXINATOR_GUESS_CONTEXT:
        return guessed_wrong(handler_input)
    elif value == ALEXINATOR_RETRY_CONTEXT:
        update_session_attributes(handler_input, "context", 0)
    return (
        handler_input.response_builder
        .speak("Schade. Es wurde gerade doch so spannend.")
        .ask("Was kann ich für dich tun?")
        .response
    )