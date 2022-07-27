import sqlite3
import logging

class SQLiteConnection:

    def __init__(self):
        
        self.connection = sqlite3.connect(":memory:")
        cursor = self.connection.cursor()

        create_table_query = '''CREATE TABLE notes (id INT PRIMARY KEY AUTOINCREMENT, description TEXT NOT NULL);'''
        # Execute a command: this creates a new table
        logging.info("Creating notes table.")
        try:
            cursor.execute(create_table_query)
            self.connection.commit()
            logging.info("Table created successfully in SQLite3")
            cursor.close()
        except:
            self.connection.rollback()
            cursor.close()
            logging.info("Table already exists.")


    def create_note(self, note):
        try:
            cursor = self.connection.cursor()
            sql = """INSERT INTO notes(description) VALUES (%s) RETURNING id;"""
            cursor.execute(sql, (note.description,))
            note_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            logging.info(f"Created note with id: {note.id}")
            return note_id
        except Exception as e:
            logging.error(e)
            self.connection.rollback()
            cursor.close()

    def update_note(self, note):
        try:
            cursor = self.connection.cursor()
            sql = """UPDATE notes SET description = %s WHERE id = %s"""
            cursor.execute(sql, (note.description, note.id))
            self.connection.commit()
            cursor.close()
            logging.info(f"Updated note with id: {note.id}")
            return str(note)
        except Exception as e:
            self.connection.rollback()
            cursor.close()

    def get_notes(self, id=None):
        cursor = self.connection.cursor()
        if id:
            try:
                query = "SELECT id, description FROM notes WHERE id = %s"
                cursor.execute(query, [id])
                note = cursor.fetchone()
                cursor.close()
                return note
            except:
                cursor.close()
                logging.error(f"Couldn't get note with id: {id}")
        else:
            try:
                query = "SELECT id, description FROM notes ORDER BY id"
                cursor.execute(query)
                notes = cursor.fetchall()
                cursor.close()
                response = {}
                for note in notes:
                    response[note[0]] = note[1]
                return response
            except:
                cursor.close()
                logging.error(f"Couldn't get notes")

    def delete_note(self, id):
        try:
            cursor = self.connection.cursor()
            sql = """DELETE FROM notes WHERE id = %s"""
            cursor.execute(sql, (id,))
            self.connection.commit()
            cursor.close()
            logging.info(f"Deleted note with id: {id}")
        except:
            self.connection.rollback()
            cursor.close()
        