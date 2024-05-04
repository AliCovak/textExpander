from my_keyboard import *
from pynput.keyboard import Listener

lock_file = "lockfile.lock"


def create_lockfile():
    if os.path.exists(lock_file):
        log.logger.error("❌ | Súbor \"lockfile.lock\" existuje. Buď predchádzajúca inštancia aplikácie "
                           "stále beží, alebo nebola ukončená korektne.")  # ❌
        choice = input("Ak predchádzajúca inštancia aplikácie už nebeží a chcete pokračovať,\n"
                       "zadajte 'p' + 'Enter' pre pokračovanie.\n"
                       "Inak stlačte iba 'Enter', ak chcete ukončiť aplikáciu bez zmeny.\n"
                       "Vasa volba: ")
        if choice.lower() == 'p':
            return True
        return False
    else:
        with open(lock_file, 'w') as file:
            file.write("LOCK")
            log.logger.info("🔒 | Subor \"lockfile.lock\" vytvoreny.")  # ℹ️
            return True


def remove_lockfile():
    if os.path.exists(lock_file):
        os.remove(lock_file)
        log.logger.info("🔓 | Subor \"lockfile.lock\" odstraneny.")  # ℹ️


def main():
    # try:
    if create_lockfile():
        with Listener(on_press=on_press, on_release=on_release) as listener:
            log.logger.info("👂🏻 | listener na stlacene klavesy aktivny")  # ℹ️
            listener.join()
            remove_lockfile()
    # finally:
    #     remove_lockfile()


if __name__ == "__main__":
    main()

print("")