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

    def search_synop_idx( self, body ):
        sql = "SELECT idx FROM synopsis WHERE body LIKE ?;"
        self.cursor.execute( sql, ('%' + body + '%',) )
        result = self.cursor.fetchall()        
        # pprint( result )
        return result[0][0] 
    
    def insert_scenario( self, content, synop_idx  ):
        sql = 'INSERT INTO scenario (content, synop_idx) VALUES (?, ?);'
        self.cursor.execute( sql, ( content, synop_idx ) )
        self.con.commit()
        

    def load_scenario( self, synop_idx ):
        sql = "SELECT content FROM scenario WHERE synop_idx = ?;"
        self.cursor.execute( sql, ( synop_idx, ) )
        result = self.cursor.fetchall()
        return result
    
    def insert_conti( self, scene, img_path, scenario_idx):
        sql = 'INSERT INTO conti (scene, img_path, scenario_idx) VALUES (?, ?, ?);'
        self.cursor.execute( sql, ( scene, img_path, scenario_idx ) )
        self.con.commit()
    
    def update_conti( self, scene, img_path, scenario_idx ):
        sql = 'UPDATE conti SET img_path = ? WHERE scene = ? AND scenario_idx = ?;'
        self.cursor.execute( sql, ( img_path, scene, scenario_idx ) )
        self.con.commit()

    def load_conti( self, scenario_idx ):
        sql = "SELECT * FROM conti WHERE scenario_idx = ?;"
        self.cursor.execute( sql, ( scenario_idx, ) )
        result = self.cursor.fetchall()
        return result

    def search_sceanrio_idx( self, content ):
        sql = "SELECT idx FROM scenario WHERE content LIKE ?;"
        self.cursor.execute( sql, ('%' + content + '%',) )
        result = self.cursor.fetchall()        
        return result[0][0] 



