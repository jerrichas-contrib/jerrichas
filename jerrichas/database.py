# Jerrichas by Jerricha@chat.cohtitan.com, Summer 2015!
# GPLv3
from io import StringIO
import sqlite3

class ParagonChatDB(object):
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = self._dict_factory
        self.session = self.conn.cursor()

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def replace_costumeparts_string():
        return """REPLACE INTO costumepart (geom, tex1, tex2, fx, displayname, region, bodyset, color1, color2, character, costume, part, bodytype, bonescale, shoulderscale, , chestscale, waistscale, hipscale, legscale)
            VALUES ('{geom}', '{tex1}', '{tex2}', '{fx}', '{displayname}', '{region}', '{bodyset}', '{color1}', '{color2}', '{character_id}', '{costume_id}', '{part}', '{bodytype}', '{shoulderscale}', '{chestscale}', '{waistscale}', '{hipscale}', '{legscale}');"""

    def _transact_query(self, sql_script):
        """
        Executes CREATE, UPDATE and DELETE queries in a BEGIN and COMMIT block, and performs basic error handling.

        :param sql_script: Generated by a CUD-like method.
        :returns: True if success, False if not.
        """
        transaction = StringIO()
        transaction.write("BEGIN TRANSACTION;")
        transaction.write(sql_script.getvalue())
        transaction.write("COMMIT;")
        try:
            self.session.executescript(sql_script.getvalue())
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.session.execute("ROLLBACK;")
            self.conn.commit()
            return False

    def get_account_names(self):
        accounts = self.session.execute("SELECT id, name FROM account")
        return accounts.fetchall()

    def get_characters(self, account):
        characters = self.session.execute("SELECT id, name, origin, class, curcostume FROM character WHERE account='{}'".format(account))
        return characters.fetchall()

    def query_replace_parts(self, costumesave, character_id, costume_id):
        """
        Performs the costume replacement query against the ParagonChat db.

        Intended use for "cherry-pick mode".

        :param costumesave: a jerrichas.CostumeCSV object
        :param chracter_id: Character ID
        :param costume_id: Costume ID

        :returns: A StringIO of an SQLite Script.
        """
        costumeparts = costumesave.get_costumeparts()
        sql_script = StringIO()
        for i in costumeparts:
            sql = """\
DELETE FROM costumepart
    WHERE character='{character_id}'
        AND costume='{costume_id}'
        AND part='{part}';
""" + replace_costumeparts_string()
            sql = sql.format(
                character_id=character_id,
                costume_id=costume_id,
                **i
            )
            sql_script.write(sql)

        return(sql_script)

    def query_replace_costume(self, costumesave, character_id, costume_id):
        """
        Writes full-costume replacement query against the ParagonChat db.

        Intended use for "batch mode".

        :param costumesave: a jerrichas.CostumeCSV object
        :param chracter_id: Character ID
        :param costume_id: Costume ID

        :returns: A StringIO of an SQLite Script.
        """
        costumeparts = costumesave.get_costumeparts()
        sql_script = StringIO()
        sql = """\
DELETE FROM costumepart
    WHERE character='{character_id}'
        AND costume='{costume_id}';"""\
        .format(
            character_id=character_id,
            costume_id=costume_id)
        sql_script.write(sql)

        for i in costumeparts:
            sql = replace_costumeparts_string().format(
                character_id=character_id,
                costume_id=costume_id,
                **i
            )
            sql_script.write(sql)
        return(sql_script)
