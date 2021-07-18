from .database import Database

class Deposit:
    def __init__(self) -> None:
        self.connection = Database("database/database.db")
        self.connection.connect()

    def deposit(self, tujuan, nominal):
        if int(nominal) > 1000000000:
            print ("[INFO]: Batas deposit hanya sampai 1 Miliar")
            return False
        else:
            data = self.connection.get("balance", "card", f"card_number={tujuan}")
            newBalance = int(data[0][0]) + int(nominal)
            self.connection.update("card", f"balance={newBalance}", f"card_number={tujuan}")
            print ("[INFO]: Berhasil deposit")
            return True