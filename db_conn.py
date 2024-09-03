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
    
    def last_scenario( self ):
        sql = "SELECT * FROM scenario ORDER BY idx DESC LIMIT 1"
        self.cursor.execute( sql )
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

    def insert_character( self, characters, scenario_idx ):
        sql = 'INSERT INTO character (characters, scenario_idx) VALUES (?, ?);'
        self.cursor.execute( sql, ( characters, scenario_idx ) )
        self.con.commit()
    
    def update_character( self, characters, scenario_idx ):
        sql = 'UPDATE character SET characters = ? WHERE scenario_idx = ?;'
        self.cursor.execute( sql, ( characters, scenario_idx ) )
        self.con.commit()
    
    def load_character( self, scenario_idx ):
        sql = "SELECT * FROM character WHERE scenario_idx = ?;"
        self.cursor.execute( sql, ( scenario_idx, ) )
        result = self.cursor.fetchall()
        return result

    def insert_concept( self, img_path, synop_idx ):
        sql =  'INSERT INTO concept ( img_path, synop_idx) VALUES ( ?, ?);'
        self.cursor.execute( sql, ( img_path, synop_idx ) )
        self.con.commit()

    def load_concept( self, synop_idx ):
        sql = "SELECT * FROM concept WHERE synop_idx = ?;"
        self.cursor.execute( sql, ( synop_idx, ) )
        result = self.cursor.fetchall()
        return result
        
    def insert_schedule( self, plan, scenario_idx ):
        sql =  'INSERT INTO schedule ( plan, scenario_idx) VALUES ( ?, ?);'
        self.cursor.execute( sql, ( plan, scenario_idx ) )
        self.con.commit()
    
    def update_schedule( self, plan, scenario_idx ):
        sql = 'UPDATE schedule SET plan = ? WHERE scenario_idx = ?;'
        self.cursor.execute( sql, ( plan, scenario_idx ) )
        self.con.commit() 

    def load_schedule( self, scenario_idx ):
        sql = "SELECT * FROM schedule WHERE scenario_idx = ?;"
        self.cursor.execute( sql, ( scenario_idx, ) )
        result = self.cursor.fetchall()
        return result
    
    def insert_budget( self, money, scenario_idx ):
        sql =  'INSERT INTO budget ( money, scenario_idx) VALUES ( ?, ?);'
        self.cursor.execute( sql, ( money, scenario_idx ) )
        self.con.commit()
    
    def update_budget( self, money, scenario_idx ):
        sql = 'UPDATE budget SET money = ? WHERE scenario_idx = ?;'
        self.cursor.execute( sql, ( money, scenario_idx ) )
        self.con.commit() 

    def load_budget( self, scenario_idx ):
        sql = "SELECT * FROM budget WHERE scenario_idx = ?;"
        self.cursor.execute( sql, ( scenario_idx, ) )
        result = self.cursor.fetchall()
        return result
