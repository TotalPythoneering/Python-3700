#!/usr/bin/env python3
# MISSION: The complete set of examples and source code for ''Python 3700: The
# SQLite Quick Start''.
# STATUS: Public Release
# VERSION: 1.0.0
# NOTES: Project: https://github.com/TotalPythoneering/Python-3700
# DATE: 2018-03-01 15:30:00
# FILE: SqlDataLogger_01.py
# AUTHOR: Randall Nagy
#
import sqlite3
""" STEP 1: Simple Data Collection """

class LogDB:

   """ Academic demonstration of adding data to the sqlite3 database """

   def __init__(self):
      self.bOpen = False
      self.conn = None
      self.curs = None

   def open(self):
        """ Connect to the LOCAL database """
        if self.bOpen == True:
                     return
        self.conn = sqlite3.connect('MyLog.db')
        self.curs = self.conn.cursor()
        self.bOpen = True
        
   def createTable(self):
        """ Create a table for the logged messages """
        self.open()
        cmd = 'create table logged \
           (timestr char(20), message char(256))'
        self.curs.execute(cmd)
        self.close()

   def dropTable(self):
        """ Remove table + data from database """
        self.open()
        cmd = 'drop table logged'
        self.curs.execute(cmd)
        self.close()

   def insertRow(self, timestr, message):
        """ Insert an arbitrary logged prefix & message """
        self.curs.execute(
            'insert into logged values(?,?)',
            [timestr, message])
        
   def selectMessages(self):
        """ Generator to enumerate values """
        self.curs.execute('select * from logged')
        for tstr, msg in self.curs.fetchall():
                     yield tstr, msg
            
   def close(self):
        if self.bOpen:
                     self.conn.commit()
        self.bOpen = False

db = LogDB()
db.createTable()
try:
    db.open()
    for ss in range(10):
        db.insertRow(
            "MyTime" + str(ss),
            "Message " + str(ss + 1))
    for zt, mgs in db.selectMessages():
        print(zt, mgs)
finally:
    db.close()
    db.dropTable()


    
