# :coding: utf-8

from flask import Flask


from pprint import pprint



app = Flask( __name__ )



@app.route( '/' )
def main_page():
    txt = '<h2><font color="red">It works!!</font></h2>'
    return txt




if __name__ == '__main__':
    app.run( host = '0.0.0.0', debug = 1, port = 5052, threaded = True  )
