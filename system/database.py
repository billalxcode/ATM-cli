import sqlite3
from os.path import isfile
from typing import ValuesView
from .cmd import CMD

class Database(object):
    def __init__(self, filename="") -> None:
        super().__init__()
        self.cmds = CMD()
        self.filename = filename
        self.connection = None
    
    def _checkFile(self):
        return isfile(self.filename)

    def connect(self):
        if self._checkFile():
            self.connection = sqlite3.connect(self.filename)
        else:
            print ("[SYSTEM]: Filename not found")
    
    def get(self, select="", table="", where=""):
        cmd = f"SELECT {select} FROM {table}"
        if int(len(where)) != 0:
            cmd += " WHERE " + where
        
        try:
            cursor = self.connection.cursor()
            result = cursor.execute(cmd)
            self.connection.commit()
            return result.fetchall()
        except Exception as e:
            print (str(e))
            return ()

    def update(self, table="", data="", where=""):
        cmd = f"UPDATE {table} SET {data}"
        if int(len(where)) != 0:
            cmd += " WHERE " + where
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(cmd)
            self.connection.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def insert(self, table, data, value):
        cmd = f"INSERT INTO {table}({data}) VALUES({value})"
        try:
            cursor = self.connection.cursor()
            cursor.execute(cmd)
            self.connection.commit()
            return True
        except Exception as e:
            return False
    # def createTable(self, cmd):
    #    if self.connection is None:
    #        print ("[ERROR]: Database belum terkoneksi")
    #        self.cmds.exit(finished=False, system=True)
    #    else:
    #        cursor = self.connection.cursor()
    #        cursor.execute(cmd)