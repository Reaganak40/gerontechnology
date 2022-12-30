

from mysql.connector import Error
import mysql.connector

from sql_shell import connect_to_db, sql_shell

def create_db():
    cxn = connect_to_db("emma_backend", user="root", password="root", create=True)
    executeScriptsFromFile("EMMA_variables_schema.sql", cxn)

def executeScriptsFromFile(filename : str, cxn : mysql.connector.MySQLConnection ):
    cursor = cxn.cursor()

    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except Error as msg:
            print(msg)

    cxn.commit()


if __name__ == "__main__":
    create_db()