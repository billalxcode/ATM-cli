from .database import Database

class Transfer:
    def __init__(self) -> None:
        self.connection = Database("database/database.db")
        self.connection.connect()

    def isValidCard(self, card):
        getcard = self.connection.get("card_number", "card", f"card_number={card}")
        if int(len(getcard)) == 1:
            return True
        else:
            return False

    def transfer(self, nominal, card, tujuan):
        if self.isValidCard(tujuan):
            balance = self.connection.get("balance", "card", f"card_number={card}")
            if balance[0][0] < int(nominal):
                print ("[INFO]: Maaf saldo anda tidak cukup, silahkan cek saldo")
                return False
            else:
                newBalance = int(balance[0][0]) - int(nominal)
                self.connection.update("card", f"balance={newBalance}", f"card_number={card}")
                balance = self.connection.get("balance", "card", f"card_number={tujuan}")
                newBalance = int(balance[0][0]) + int(nominal)
                self.connection.update("card", f"balance={newBalance}", f"card_number={tujuan}")
                print ("[INFO]: Saldo berhasil di transfer")
                return True
        else:
            print ("[INFO]: Rekening tujuan tidak ditemukan")
            return False