# TODO: trouver un meilleur nom pour ce fichier

import sqlite3


class SQLiteOutput:

    TABLE_SCHEMA = {"badge" : "CREATE TABLE IF NOT EXISTS badge\
                        (uniqueid INTEGER PRIMARY KEY,\
                        Id INTEGER, \
                        Nom TEXT,\
                        Prenom TEXT,\
                        Date DATE)" }

    def __init__(self, db, table):
        self.db = db
        if table in self.TABLE_SCHEMA.keys():
            self.table = table
            self._create_table()
        else:
            raise ValueError("No schema found for this table", table)

    def _create_table(self):
        with sqlite3.connect(self.db) as cnx:
            cnx.cursor().execute(self.TABLE_SCHEMA[self.table])

    def _drop(self):
        with sqlite3.connect(self.db) as cnx:
            cnx.cursor().execute("DROP TABLE IF EXISTS {}".format(self.table))

    def insert(self, val_dict):
        with sqlite3.connect(self.db) as cnx:
            query = {"table" : self.table,
                     "columns" : "({})".format(", ".join(val_dict.keys())),
                     "val_placeholder" : "({})".format(", ".join(["?"]*len(val_dict)))}
            cnx.cursor().execute("INSERT INTO {table} {columns} VALUES {val_placeholder}".format(**query),
                                 tuple(val_dict.values()))

    def update(self, keys_dict , val_dict):
        with sqlite3.connect(self.db) as cnx:
            query = {"table" : self.table,
                     "values" : "{}".format(', '.join('{}="{}"'.format(k,v) for (k,v) in val_dict.items())),
                     "keys" : "{}".format(' AND '.join('{}="{}"'.format(k,v) for (k,v) in keys_dict.items()))
                     }
            print("UPDATE {table} SET {values} WHERE {keys}".format(**query))
            cnx.cursor().execute("UPDATE {table} SET {values} WHERE {keys}".format(**query))

    def select(self, val_dict , key_set):
        with sqlite3.connect(self.db) as cnx:
            query = {"table" : self.table,
                     "keys" : ", ".join(list(key_set)),
                     "val_placeholder" : "{}".format(' AND '.join('{}="{}"'.format(k,v) for (k,v) in val_dict.items()))}
            cursor=cnx.cursor()
            cursor.execute("SELECT {keys} FROM {table} WHERE {val_placeholder}".format(**query))
            return dict(zip(list(key_set),cursor.fetchall()[0]))

    def select_max_unique_id(self):
        with sqlite3.connect(self.db) as cnx:
            cursor=cnx.cursor()
            cursor.execute("SELECT MAX(uniqueid) FROM badge")
            return cursor.fetchall()[0]
