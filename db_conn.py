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
    
    def insert_scenario( self, content, synop_idx, created  ):
        sql = 'INSERT INTO scenario (content, synop_idx, created) VALUES (?, ?, ?);'
        self.cursor.execute( sql, ( content, synop_idx, created ) )
        scenario_idx = self.cursor.lastrowid
        self.con.commit()
        return scenario_idx
    
    def search_scenario_idx( self, content ):
        if len(content) > 100:
            content = content[:100]
        sql = "SELECT idx FROM scenario WHERE content LIKE ?;"
        self.cursor.execute( sql, ('%' + content + '%',) )
        result = self.cursor.fetchall()        
        return result
    
    def search_created( self, idx ):
        sql = "SELECT created FROM scenario WHERE idx=?;"
        self.cursor.execute( sql, ( idx, ))
        result = self.cursor.fetchall()     
        return result[0][0]
        

    def load_scenario( self, synop_idx ):
        sql = "SELECT content FROM scenario WHERE (synop_idx = ? OR synop_idx IS NULL) ORDER BY idx DESC LIMIT 1;"
        self.cursor.execute( sql, ( synop_idx, ) )
        result = self.cursor.fetchall()
        return result
    
    def last_scenario( self ):
        sql = "SELECT * FROM scenario ORDER BY idx DESC LIMIT 1"
        self.cursor.execute( sql )
        result = self.cursor.fetchall()
        return result
    
    def insert_div_scene(self, num, content, scenario_idx):
        sql = 'INSERT INTO div_scenario (num, content, scenario_idx) VALUES (?, ?, ?);'
        self.cursor.execute( sql, ( num, content, scenario_idx ) )
        self.con.commit()
    
    def load_div_scene(self, scenario_idx):
        sql = "SELECT * FROM div_scenario WHERE scenario_idx = ?;"
        self.cursor.execute( sql, ( scenario_idx, ) )
        result = self.cursor.fetchall()
        return result
    
    def search_div_idx(self, num, scenario_idx):
        sql = "SELECT idx FROM div_scenario WHERE num = ? AND scenario_idx = ?;"
        self.cursor.execute( sql, ( num, scenario_idx, ) )
        result = self.cursor.fetchall()
        return result[0][0]

    def insert_conti( self, img_path, div_idx):
        sql = 'INSERT INTO conti (img_path, div_idx) VALUES (?, ?);'
        self.cursor.execute( sql, ( img_path, div_idx ) )
        self.con.commit()
    
    def delete_conti( self, scenario_idx):
        sql = 'DELETE FROM conti WHERE scenario_idx = ?;'
        self.cursor.execute( sql, ( scenario_idx, ) )
        self.con.commit()
    
    def load_conti( self, div_idx ):
        sql = "SELECT img_path FROM conti WHERE div_idx = ?;"
        self.cursor.execute( sql, ( div_idx, ) )
        result = self.cursor.fetchall()
        return result[0][0]

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
    
    def insert_ppt( self, ppt_path, scenario_idx ):
        sql =  'INSERT INTO ppt ( ppt_path, scenario_idx) VALUES ( ?, ?);'
        self.cursor.execute( sql, ( ppt_path, scenario_idx ) )
        self.con.commit()
    
    def update_ppt( self, ppt_path, scenario_idx ):
        sql = 'UPDATE ppt SET ppt_path = ? WHERE scenario_idx = ?;'
        self.cursor.execute( sql, ( ppt_path, scenario_idx ) )
        self.con.commit() 
    
    def load_ppt_path(self, scenario_idx):
        sql = "SELECT ppt_path FROM ppt WHERE scenario_idx = ?;"
        self.cursor.execute( sql, ( scenario_idx, ) )
        result = self.cursor.fetchall()
        return result

    def login( self, login_id, login_pw ):
        sql = 'SELECT username, passwd FROM users WHERE username = "{}";'.format( login_id )
        self.cursor.execute( sql )
        result = self.cursor.fetchall()
        if not result:
            return False
        if result[0]:
            if result[0][1] == login_pw:
                return True
        return False


