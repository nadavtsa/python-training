import sqlite3

class Manager:
    def __init__(self):
        self.connection = sqlite3.connect('data.db')

    def __del__(self):
        self.connection.close()
