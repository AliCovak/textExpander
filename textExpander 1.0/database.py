import sys

import my_keyboard
import os
import json


test_database = {
    ";hw": "Hello hw World!\n\ngmhw hw",
    ";gm": "Good\nMorning!",
    ";euro": "\u20AC",
    ":id:": "https://www.mojafirma.sk/mojaappka/$s/open",
    ":jira1:": "https://jira.mojafirma.sk/jira/projects/$s",
    ":jira2:": "<a href=https://jira.mojafirma.sk/jira/projects/$s>$s</a>",
    ":phone:": "https://www.mojafirma.sk/call?phone=$s",
    ":test:": "ok-$s"
}


def load_database_from_json(filename):
    my_keyboard.log.logger.info('🧩 | nacitava sa databaza z JSON suboru: "' + os.path.realpath(filename) + '"')  # ✏️ℹ️
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        my_keyboard.log.logger.critical(
            '🔥 | nespravny format JSON suboru: "' + os.path.realpath(
                filename) + '"')  # 🔥
        sys.exit(100)
    except FileNotFoundError:
        my_keyboard.log.logger.critical(f"🔥 | subor obsahujuci skratky a ich texty \"{filename}\" sa nenasiel")  # 🔥
        sys.exit(10)


def load_configuration_from_json(filename):
    my_keyboard.log.logger.info('⚙️ | nacitava sa konfiguracia z JSON suboru: "' + os.path.realpath(filename) + '"')  # ✏️ℹ️
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        my_keyboard.log.logger.critical(
            '🔥 | nespravny format JSON suboru: "' + os.path.realpath(
                filename) + '"')  # 🔥
        sys.exit(111)
    except FileNotFoundError:
        my_keyboard.log.logger.critical(f"🔥 | konfiguracny subor \"{filename}\" sa nenasiel")  # 🔥
        sys.exit(11)


def get_key_length_max(database):
    max_value = 0
    for key in database.keys():
        if len(key) > max_value:
            max_value = len(key)
    return max_value
