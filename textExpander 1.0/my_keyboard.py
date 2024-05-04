import ctypes
import time

import logger as log
from database import *
from pynput.keyboard import Controller, Key
import sys
import pyperclip

# text_expander_db = test_database
text_expander_db = load_database_from_json("shortcuts.json")
text_expander_config = load_configuration_from_json("default-configuration.json")

key_length_max = get_key_length_max(text_expander_db)
log.logger.debug(f"📦 | key_length_max = \"{key_length_max}\"")  # 🪲

user_typed = ""
user_typed_length_max = key_length_max + 5
user_typed_length_extra = 160
user_typing = True
replacement_text_length = -1
keyboard = Controller()
indicator = '$'
placeholder = "$s"
replacement_text_with_placeholder = ""
shift_enter = bool(text_expander_config.get("shift_enter_bool"))
clipboard_char = bool(text_expander_config.get("clipboard_char_bool"))
# default_char = str(text_expander_config.get("default_char_str"))[0]
default_char = str(text_expander_config.get("default_char_str", "_"))[0]
off_shortcut = str(text_expander_config.get("off_shortcut"))
off_key_esc = bool(text_expander_config.get("off_key_escape"))


console_debug_mode = bool(text_expander_config.get("console_debug_mode"))
if console_debug_mode:
    log.logger.warning(f"⚠️⚠️⚠️ | console_debug_mode = ON")  # ⚠️
    log.console_handler = log.console_handler.setLevel(log.logging.DEBUG)
else:
    log.console_handler = log.console_handler.setLevel(log.logging.INFO)


inputs = {
    96: "0",
    97: "1",
    98: "2",
    99: "3",
    100: "4",
    101: "5",
    102: "6",
    103: "7",
    104: "8",
    105: "9",
}

escape_chars = {
    '\n': Key.enter,
    '\r': Key.enter,
    '\t': Key.tab}


def update_user_input(key):
    global user_typed
    if key == Key.backspace:
        user_typed = user_typed[:-1]  # odstrani posledny znak
    elif key == Key.space:
        user_typed += " "  # prida medzeru
    elif isinstance(key, str):  # prida iba alfanumericky znak (pismeno alebo cislo)
        user_typed += key
        if replacement_text_with_placeholder == "":
            user_typed = user_typed[-user_typed_length_max:]  # uklada limitovany pocet znakov
            log.logger.debug(f"✏️ | user_typed_length_max = \"{user_typed_length_max}\"")  # 🪲
        else:
            user_typed = user_typed[-user_typed_length_extra:]  # uklada extra pocet znakov
            log.logger.debug(f"✏️✏️✏️ | user_typed_length_extra = \"{user_typed_length_extra}\"")  # 🪲


def check_exit_conditions(key):
    global off_shortcut
    global off_key_esc
    if off_shortcut in user_typed:
        # log.logger.info(f"👋🏻 | Bolo napisane \"{off_shortcut}\" = ukoncenie programu")  # ℹ️
        # sys.exit()
        for _ in user_typed:
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)

        off = 'dovi dopo - aplikacia ukoncena pouzivatelom'
        keyboard.type(off)

        time.sleep(3)
        for _ in off:
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)

        log.logger.info(off)  # ✏️ℹ️
        sys.exit(0)  # ukoncenie aplikacie s kodom 0 (bez chyby)

    if key == Key.esc and off_key_esc:
        log.logger.info(f"👋🏻 | \'{key}\' = ukoncenie programu")  # ℹ️
        sys.exit()


# time.sleep(2)
# pyperclip.copy("ahoj\ndovi")
# with keyboard.pressed(Key.ctrl):
#     keyboard.press('v')
#     keyboard.release('v')


def keyboard_type(text):
    global replacement_text_length
    for char in text:
        char = escape_chars.get(char, char)
        try:
            if char == Key.enter and shift_enter:
                replacement_text_length += 1
                with keyboard.pressed(Key.shift):
                    keyboard.tap(Key.enter)
            else:
                keyboard.tap(char)
        except ctypes.ArgumentError:
            if clipboard_char:
                pyperclip.copy(char)
                replacement_text_length += 1
                with keyboard.pressed(Key.ctrl):
                    keyboard.press('v')
                    keyboard.release('v')
                log.logger.debug(
                    f"⚠️ | nepodporovany znak \'{char}\' bol vlozeny pomocou pouzitia systemovej schranky")  # 🪲️
            else:
                keyboard.tap(default_char)
                log.logger.debug(f"⚠️ | nepodporovany znak \'{char}\' bol nahradeny znakom: \'{default_char}\'")  # 🪲️


def check_text_expander_db():
    global user_typed, replacement_text_with_placeholder, replacement_text_length
    log.logger.debug(f"🔍 | hlada v databaze: \"{user_typed}\"")  # 🪲
    for text_to_be_replaced, replacement_text in text_expander_db.items():

        if user_typed.endswith(text_to_be_replaced):
            log.logger.info(f"🚀 | aktivacia na zaklade skratky: \'{text_to_be_replaced}\'")  # ℹ️

            if placeholder in replacement_text:
                replacement_text_with_placeholder = replacement_text
                user_typed = text_to_be_replaced
                keyboard.tap(indicator)
                log.logger.info(f"⌨️ | program natuka(l) \'{indicator}\'")  # ℹ️
                log.logger.debug(
                    f"📦 | replacement_text_with_placeholder = \"{replacement_text_with_placeholder}\"")  # 🪲
                log.logger.debug(f"📦 | user_typed = \"{user_typed}\"")  # 🪲
            else:
                user_typed = ""
                # nezaznamenava pre user_typed
                replacement_text_length = len(text_to_be_replaced) + len(replacement_text)

                # keyboard.type("\b" * (len(text_to_be_replaced)) + replacement_text)
                keyboard_type("\b" * (len(text_to_be_replaced)) + replacement_text)

                log.logger.info(f"⌨️ | program mal natukat: \n"
                                f"---\n"
                                f"\"{replacement_text}\"\n"
                                f"---")  # ℹ️

                log.logger.debug(f"‍📦 | user_typed = \"{user_typed}\" ")  # 🪲


def process_replacement_text_with_placeholder():
    global replacement_text_length, user_typed, replacement_text_with_placeholder
    replacement_text_final = replacement_text_with_placeholder.replace(
        placeholder,
        user_typed[(user_typed.find(indicator) + 1):])
    # nezaznamenava pre user_typed
    replacement_text_length = len(user_typed) + len(replacement_text_final) + 1  # +1 -> potvrdzovacia klavesa

    # testujem
    log.logger.debug(f"‍📦 | user_typed = \"{user_typed}\", {len(user_typed)}")  # 🪲
    log.logger.debug(f"‍📦 | replacement_text_final = \"{replacement_text_final}\", {len(replacement_text_final)}")  # 🪲

    keyboard_type("\b" * (len(user_typed) + 1) + replacement_text_final)  # +1 -> potvrdzovacia klavesa

    log.logger.info(f"⌨️ | program mal natukat: \n"
                    f"---\n"
                    f"\"{replacement_text_final}\"\n"
                    f"---")  # ℹ️


def on_press(key):
    global replacement_text_length, user_typed, replacement_text_with_placeholder
    if replacement_text_length >= 0:
        return
    user_typed_old = user_typed
    try:
        if hasattr(key, 'vk') and key.vk is not None and 96 <= key.vk <= 105:
            log.logger.debug(f'⬇️ | stlacena alfanumericka klavesa na numerickej klavesnici: {inputs[key.vk]}')  # 🪲
            update_user_input(inputs[key.vk])
        else:
            log.logger.debug(f"⬇️ | stlacena alfanumericka klavesa \'{key.char}\'")  # 🪲
            update_user_input(key.char)
    except AttributeError:
        log.logger.debug(f"⬇️ | stlaceny specialny klaves \'{key}\'")  # 🪲
        update_user_input(key)
    finally:
        if user_typed_old != user_typed:
            log.logger.debug(f"‍📦 | user_typed = \"{user_typed}\"")  # 🪲

    check_exit_conditions(key)

    if user_typed != "" and replacement_text_with_placeholder == "":
        check_text_expander_db()
    elif len(user_typed) > 0:
        log.logger.debug(f"📦 | {indicator} = \"{user_typed[(user_typed.find(indicator) + 1):]}\"")  # 🪲

        # OPTION 1: vymaze, co pouzivatel napisal
        if user_typed.find(indicator) == -1:
            keyboard.type("\b" * (len(user_typed)))

            user_typed = ""
            replacement_text_with_placeholder = ""

        if hasattr(key, "char") and key.char == ";":
            user_typed = user_typed[:-1]

            # OPTION 2: napise nahradzujuci text, vratane zastupneho symbolu
            if user_typed[-1] == indicator:
                # nezaznamenava pre user_typed
                replacement_text_length = len(
                    user_typed) + 1 + len(replacement_text_with_placeholder)  # +1 -> potvrdzovacia klavesa
                keyboard.type(
                    "\b" * (len(user_typed) + 1) + replacement_text_with_placeholder)  # +1 -> potvrdzovacia klavesa
            else:
                # OPTION 3: napise nahradzujuci text, vratane premennej
                process_replacement_text_with_placeholder()

            user_typed = ""
            replacement_text_with_placeholder = ""
            log.logger.debug(f"‍📦 | replacement_text_with_placeholder = \"{replacement_text_with_placeholder}\" ")  # 🪲
            log.logger.debug(f"‍📦 | user_typed = \"{user_typed}\" ")  # 🪲

    elif len(user_typed) == 0 and replacement_text_with_placeholder != "":
        replacement_text_with_placeholder = ""
        log.logger.debug(f"‍📦 | replacement_text_with_placeholder = \"{replacement_text_with_placeholder}\" ")  # 🪲


def on_release(key):
    global replacement_text_length
    if replacement_text_length >= 0:
        replacement_text_length -= 1
        return

    try:
        if hasattr(key, 'vk') and key.vk is not None and 96 <= key.vk <= 105:
            log.logger.debug(f'⬇️ | stlacena alfanumericka klavesa na numerickej klavesnici: {inputs[key.vk]}')  # 🪲
        else:
            log.logger.debug(f"⬆️ | \'{key.char}\' uvolnene")  # 🪲
    except AttributeError:
        log.logger.debug(f"⬆️ | \'{key}\' uvolnene")  # 🪲
