from .database import Database

class Withdraw:
    def __init__(self) -> None:
        self.connection = Database("database/database.db")
        self.connection.connect()

    def get(self, card, nominal=0):
        if int(nominal) <= 10000:
            print ("[INFO]: Minimal penarikan 10 ribu")
            return False
        else:
            data = self.connection.get("balance", "card", f"card_number={card}")
            balance = data[0][0]
            if int(nominal) < balance:
                newBalance = balance - int(nominal)
                self.connection.update("card", f"balance={newBalance}", where=f"card_number={card}")
                print ("[INFO]: Penarikan berhasil")
                return True
            else:
                print ("[INFO]: Maaf saldo anda kurang, silahkan cek saldo")
                return False