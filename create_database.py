import json
from typing import List


def save_to_file(data: dict):
    json_object = json.dumps(data, indent=4)
    file_name = "temp.txt"
    with open(file_name, "w") as file:
        file.write(json_object)
        file.close()
    print("Successfully saved file!")
    fix_file(file_name)


def fix_file(filename: str):
    lines = []
    with open(filename, "r") as file:
        file_lines = file.readlines()
        for line in file_lines:
            lines.append(line.replace("true", "True").replace("false", "False"))
        file.close()
    with open(filename, "w") as file:
        file.writelines(lines)
        file.close()


def create_database_from_file(filename: str):
    data = {}
    all_traits = []
    rough_persons = []
    all_questions = []
    with open(filename, "r") as file:
        # Persons
        while True:
            name = file.readline().strip().replace("\n", '')
            traits = file.readline().replace("\n", '').split(",")
            if name == '' or traits == '':
                break
            rough_persons.append(format_person(name, traits))
            all_traits.extend(traits)

        # Questions
        while True:
            trait = file.readline().strip().replace("\n", '')
            questions = file.readline().replace("\n", '').split(",")
            if trait == '' or questions == '':
                break
            all_questions.append({"questions": questions, "property": trait})
        file.close()

    all_traits = list(set(all_traits))
    persons = update_persons(rough_persons, all_traits)
    data["persons"] = persons
    data["questions"] = all_questions
    save_to_file(data)


def create_database():
    data = {}
    all_traits = []

    # Persons
    rough_persons = []
    while True:
        print("Add another person? (y/n)")
        cont = input().lower()
        if cont == 'y' or cont == "yes":
            person, traits = create_person()
            rough_persons.append(person)
            all_traits.extend(traits)
        elif cont == 'n' or cont == "no":
            break
        else:
            print("Invalid input!")
    all_traits = list(set(all_traits))

    # Update Persons
    persons = update_persons(rough_persons, all_traits)

    # Questions
    questions = []
    for trait in all_traits:
        questions.append(create_question(trait))

    # Format and save
    data["persons"] = persons
    data["questions"] = questions
    save_to_file(data)


def update_persons(rough_persons: List, all_traits: List):
    persons = []
    for person in rough_persons:
        persons.append(update_person(person, all_traits))
    return persons


def create_question(trait: str):
    questions = []
    print(f"Enter questions for trait '{trait}': (Enter 'stop' to stop)")
    while True:
        question = input()
        if question.lower() == "stop":
            break
        questions.append(question)
    return {"questions": questions, "property": trait}


def create_person():
    print("Enter character name:")
    name = input()
    traits = []
    print("Enter character traits: (Enter 'stop' to stop)")
    while True:
        trait = input()
        if trait.lower() == "stop":
            break
        traits.append(trait)
    return format_person(name, traits), traits


def update_person(person: dict, traits):
    for trait in traits:
        if trait not in person.keys():
            person[trait] = False
    return person


def format_person(name: str, traits: List[str]):
    data = {"name": name}
    for trait in traits:
        data[trait] = True
    return data


if __name__ == '__main__':
    create_database()
    create_database_from_file("C:/Users/reyof/PycharmProjects/Alexinator/database.txt")
