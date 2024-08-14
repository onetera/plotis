# :coding: utf-8

from pprint import pprint
import sqlite3


class DBconn:
    def __init__( self ):
        self.con = sqlite3.connect( './main.db' )
        self.cursor = self.con.cursor()
        self.cursor.execute("PRAGMA case_sensitive_like = ON")
        
    def execute( self, sql ):
        self.cursor.execute( sql )
        result = self.cursor.fetchall() 
        pprint( result )
        return result
    
    
    def insert_synop( self, body, keywords  ):        
        sql = 'INSERT INTO synopsis ( body , keywords ) VALUES(  "{}", "{}" );'.format(  body ,keywords ) 
        self.cursor.execute( sql )
        self.con.commit()
        
        
    def search_synop( self, word ):
        sql = "SELECT * FROM synopsis WHERE keywords LIKE '%{}%';".format( word )
        self.cursor.execute( sql )
        result = self.cursor.fetchall()        
        pprint( result )
        return result 

    def last_synop( self ):
        sql = "SELECT * FROM synopsis ORDER BY idx DESC LIMIT 1"
        self.cursor.execute( sql )
        result = self.cursor.fetchall()
        return result






