import time
import getpass
from system.cmd import CMD
from system.database import Database
from system.account import Account
from system.withdraw import Withdraw
from system.transfer import Transfer
from system.deposit import Deposit

class ATM(object):
    def __init__(self) -> None:
        super().__init__()
        self.database = Database("database/database.db")
        self.database.connect()
        self.cmd = CMD()
        self.account = Account()
        self.withdraw = Withdraw()
        self.tf = Transfer()
        self.deposit = Deposit()

        self.isLogin = False
        self.cardNumber = ""

    def login(self):
        count = 0
        while True:
            count += 1
            self.cmd.clear()
            number = input("Masukan nomor rekening: ")
            pin = input("Masukan pin rekening: ")
            if (int(len(number)) == 0) or (int(len(pin)) == 0):
                print ("[INFO]: Masukan nomor rekening atau pin!")
            else:
                if self.account.isValidCard(number, pin) is True:
                    self.isLogin = True
                    self.cardNumber = number
                    break
                else:
                    time.sleep(2)
        return True

    def logout(self):
        self.isLogin = False

    def tarikTunai(self):
        while True:
            self.cmd.clear()
            nominal = input("Masukan nominal penarikan: ")
            withdraw = self.withdraw.get(self.cardNumber, nominal)
            if withdraw is True:
                while True:
                    y = getpass.getpass("Tekan enter untuk kembali")
                    if y == "": return True
                    else: continue
            else:
                time.sleep(2)

    def infoSaldo(self):
        while True:
            self.cmd.clear()
            data = self.database.get("balance", "card", f"card_number={self.cardNumber}")
            print (f"Kamu memiliki saldo sebesar: {data[0][0]}")
            y = getpass.getpass("Tekan enter untuk kembali")
            if y == "": return True
            else: continue

    def transfer(self):
        while True:
            self.cmd.clear()
            rekening = input("Masukan rekening tujuan: ")
            nominal = input("Masukan nominal: ")
            y = input("Apakah tujuan benar? (Y/n): ")
            if y.lower() == "y":
                if self.tf.transfer(nominal, self.cardNumber, rekening):
                    while True:
                        y = getpass.getpass("Tekan enter untuk kembali")
                        if y == "": return True
                        else: continue
                else: time.sleep(3)
            else:
                continue

    def tambahSaldo(self):
        while True:
            self.cmd.clear()
            nominal = input("Masukan jumlah: ")
            if self.deposit.deposit(self.cardNumber, nominal):
                while True:
                    y = getpass.getpass("Tekan enter untuk kembali")
                    if y == "": return True
                    else: continue
            else: time.sleep(3)

    def ubahPin(self):
        while True:
            self.cmd.clear()
            pinLama = input("Masukan pin lama: ")
            pinBaru = input("Masukan pin baru: ")
            cpinBaru = input("Konfirmasi pin baru: ")
            getOldPin = self.database.get("pin", "users", f"pin={pinLama}")
            if int(len(getOldPin)) == 0:
                print ("[INFO]: Maaf pin salah, silahkan coba lagi")
                time.sleep(3)
                continue
            else:
                if int(len(pinBaru)) == 4:
                    if pinBaru == cpinBaru:
                        self.database.update("users", f"pin={pinBaru}", f"pin={pinLama}")
                        self.database.update("card", f"card_pin={pinBaru}", f"card_pin={pinLama}")
                        print ("[INFO]: Pin berhasil diubah")
                        while True:
                            y = getpass.getpass("Tekan enter untuk kembali")
                            if y == "": return True
                            else: continue
                    else:
                        print ("[INFO]: Pin baru tidak cocok")
                        time.sleep(3)
                        continue
                else:
                    print ("[INFO]: Pin terdiri dari 4 digit")
                    time.sleep(3)
                    continue

    def buatRekening(self):
        while True:
            self.cmd.clear()
            username = input("Masukan nama unik: ")
            nama = input("Masukan nama lengkap: ")
            pin = input("Masukan pin: ")
            if (int(len(username)) == 0) or (int(len(nama)) == 0) or (int(len(pin)) == 0):
                print ("[INFO]: Username, nama, pin tidak boleh kosong!")
                continue
            else:
                if self.account.createCredit(username, nama, pin):
                    while True:
                        enter = input("[INFO[: Tekan 'enter' untuk kembali")
                        if enter == "":
                            return True
            y = input("Ulangi? (Y/n): ")
            if y.lower() == "y": continue
            else: break

    def mainmenu(self):
        while True:
            self.cmd.clear()
            menu = ["Tarik tunai", "Info saldo", "Transfer", "Tambah saldo", "Ubah pin"]
            print ("Menu: ")
            for i in range(0, int(len(menu))):
                print (f"\t{i+1}). {menu[i]}")
            print ("\t0). Logout")

            i = input("Pilih: ")
            if i == "1" or i == "01":
                self.tarikTunai()
            elif i == "2" or i == "02":
                self.infoSaldo()
            elif i == "3" or i == "03":
                self.transfer()
            elif i == "4" or i == "04":
                self.tambahSaldo()
            elif i == "5" or i == "05":
                self.ubahPin()
            elif i == "0" or i == "00":
                self.isLogin = False
                break

    def main(self):
        self.cmd.clear()
        print ("""\t ATM:
\t  ╔╗╔┬ ┬┌─┐┌─┐┌┐┌┌┬┐┌─┐┬─┐┌─┐
\t  ║║║│ │└─┐├─┤│││ │ ├─┤├┬┘├─┤
\t  ╝╚╝└─┘└─┘┴ ┴┘└┘ ┴ ┴ ┴┴└─┴ ┴
\t         ATM Based CLI""")
        time.sleep(5)
        while True:
            self.cmd.clear()
            print ("Menu: ")
            print ("\t1). Login")
            print ("\t2). Buat rekening")
            print ("\t0). Exit")
            i = input("Pilih: ")
            if i == "1" or i == "01":
                if self.login():
                    self.mainmenu()
            elif i == "2" or i == "02":
                self.buatRekening()
            elif i == "0" or i == "00":
                self.cmd.exit(noLog=True)

if __name__ == "__main__":
    atm = ATM()
    atm.main()