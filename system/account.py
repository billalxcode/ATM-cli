import random
from .database import Database

class Account:
    def __init__(self) -> None:
        self.connection = Database("database/database.db")
        self.connection.connect()

        self.alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

    def _generateCard(self):
        return random.randint(00000000000, 99999999999)

    def randomalphabet(self):
        length = random.randint(1, 5)
        alphabet = ""
        for i in range(0, length):
            alphabet += random.choice(list(self.alphabet))
        return alphabet

    def isValidCard(self, card_number, card_pin):
        fetchAll = self.connection.get("card, pin", "users", f"card={card_number}")
        if len(fetchAll) != 0:
            pin = fetchAll[0][1]
            if card_pin == str(pin):
                return True
            else:
                print ("[INFO]: Maaf pin anda salah")
                return False
        else:
            print ("[INFO]: Kartu tidak ditemukan, mohon maaf")
            return False

    def createCredit(self, username, name, pin):
        if int(len(pin)) == 4:
            username += self.randomalphabet()
            card = self._generateCard()
            self.connection.insert("users", "id, username, name, pin, card", f"NULL, '{username}', '{name}', {pin}, {card}")
            self.connection.insert("card", "id, card_number, card_pin, balance", f"NULL, {card}, {pin}, 0")
            print (f"USERNAME: {username}\nCARD: {card}\nPIN: {pin}")
        else:
            print ("[INFO]: Pin harus 4 digit")
            return False