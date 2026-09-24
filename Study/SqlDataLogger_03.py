#!/usr/bin/env python3
# MISSION: The complete set of examples and source code for ''Python 3700: The
# SQLite Quick Start''.
# STATUS: Public Release
# VERSION: 1.0.0
# NOTES: Project: https://github.com/TotalPythoneering/Python-3700
# DATE: 2018-03-01 15:30:00
# FILE: SqlDataLogger_03.py
# AUTHOR: Randall Nagy
#

# File: SqlDataLogger_03.py
# Created 2016/08/27

import sqlite3
from datetime import datetime as zdate

""" STEP 3: Adding Update, Delete, and ROW COUNT """

class LogDB:

     """ Demonstration of sqlite3 database encapsulation """

     def __init__(self):
         self.bOpen = False
         self.conn = None
         self.curs = None
         
    def open(self):
        """ Connect to the LOCAL database """
        if self.bOpen == True:
            return
        self.conn = sqlite3.connect('MyLogged.db')
        self.curs = self.conn.cursor()
        self.bOpen = True

        
    def createTable(self):
        """ Create a table for the logged messages """
        self.open()

        cmd = 'create table logged \
           (lid INTEGER PRIMARY KEY AUTOINCREMENT, \
           timestr char(20), \
           message char(256))'
        self.curs.execute(cmd)
        self.close()


    def dropTable(self):
        """ Remove table + data from database """
        self.open()
        cmd = 'drop table logged'
        self.curs.execute(cmd)
        self.close()


    def insertRow(self, timestr, message):
        """ Insert an arbitrary logged-prefix & message """
        self.curs.execute(\
            'insert into logged (timestr, message) values(?,?)',
            [timestr, message])

        
    def selectMessages(self):
        """ Generator to enumerate thru the discovered values """
        self.curs.execute('select * from logged')

        for key, tstr, msg in self.curs.fetchall():
            yield key, tstr, msg


    # NEW
    def updateRow(self, pk, timestr, message):
        res = self.curs.execute(
            "UPDATE logged \
            SET timestr = ?, message = ? \
            WHERE lid = ?", [timestr, message, pk])
        return res.rowcount


    # NEW
    def deleteRow(self, pk):
        res = self.curs.execute(
            "DELETE from logged WHERE lid = ?", [pk])
        return res.rowcount


    # NEW
    def dbSize(self):
        res = self.curs.execute(
            "SELECT count(*) FROM logged")
        return res.fetchone()[0] # returns a tuple ...


    def close(self):
        if self.bOpen:
            self.conn.commit()
        self.bOpen = False


db = LogDB()
db.createTable()
try:
    db.open()
    for ss in range(10):
        # CREATE
        db.insertRow(
            zdate.utcnow(),
            "Message " + str(ss + 1))
    for num, zt, mgs in db.selectMessages():
        print(num, zt, mgs)
        
    for ss in range(10, 20):
        # UPDATED
        num = db.updateRow(
            ss - 10 + 1,
            zdate.utcnow(),
            "Message " + str(ss + 1))
        print("Updated", num, "row.")

    for num, zt, mgs in db.selectMessages():
        print("Updated:", num, zt, mgs)

    print("Database has", db.dbSize(), "rows.")

    for ss in range(10):
        db.deleteRow(ss + 1) # SQL is 1's based ...

    print("Database has", db.dbSize(), "rows.")

finally:
    db.close()
    db.dropTable()




