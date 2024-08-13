# :coding: utf-8

from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import markdown

import os
import pickle
import ast

import pprint

import core
import importlib
importlib.reload(core)

import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask( __name__ )

app.config['UPLOAD_FOLDER'] = './tmp'
app.config['SESSION_TYPE'] = 'filesystem'  # 세션을 파일 시스템에 저장
Session(app)

@app.route( '/' )
def main_page():
    return render_template( 'main.html' )

@app.route( '/synopsis', methods=[ 'GET', 'POST' ])
def synopsis():
    if request.method == 'POST':

        keywords   = request.form.get( 'synopsis', '' )
        load_synop = request.form.get( 'load_synop', '' )
        
        synop_path = os.path.join(app.config['UPLOAD_FOLDER'], 'synop.txt')
        preprod_ai = core.PreprodAI()

        if load_synop:
            with open(  synop_path ) as f:
                data = f.read()
                preprod_ai.synop = data
        else:

            if not keywords:
                logging.error( 'No Keywords' )
                return redirect( request.url )
            
            logging.info( 'Start to make synopsis list from keywords' )
            preprod_ai.create_synop(keywords)
            

            with open( synop_path , 'w' ) as f:
                f.write( preprod_ai.synop )

        return render_template( 'synopsis.html', synopsis_result= preprod_ai.synop  )

    return render_template( 'synopsis.html' )

@app.route( '/scenario', methods = ['GET', 'POST'] )
def scenario():
    preprod_ai = core.PreprodAI()

    scenario      = request.form.get( 'scenario'        , '' )
    load_scenario = request.form.get( 'load_scenario'   , '' )
    
    synop_path      = os.path.join(app.config['UPLOAD_FOLDER'], 'synop.txt'     )
    loc_path        = os.path.join(app.config['UPLOAD_FOLDER'], 'location.txt'  )
    scenario_path   = os.path.join(app.config['UPLOAD_FOLDER'], 'scenario.txt'  )


    if load_scenario:
        if os.path.exists( synop_path ):
            with open( synop_path  ) as f:
                preprod_ai.synop = f.read( )

        if os.path.exists( loc_path ):
            with open( loc_path ) as f:
                loc_data = f.read().strip()
            preprod_ai.loc = ast.literal_eval(loc_data)                    
            logging.info( 'location file exists' )
        else:
            logging.info( 'location file does not exists' )
            preprod_ai.create_location()

        if os.path.exists( scenario_path ):
            with open( scenario_path ) as f:
                scenario_data = f.read().strip()
            preprod_ai.scenario = scenario_data 
            logging.info( 'scenario file exists' )
    else:
        logging.info( 'scenario file does not exists' )
        preprod_ai.write_scene()

    scenario = markdown.markdown( preprod_ai.scenario )



    return render_template( 
                                'scenario.html', 
                                synopsis_result=preprod_ai.synop, 
                                #scenario_result=preprod_ai.scenario 
                                scenario_result = scenario
                            )
        
@app.route( '/conti', methods = ['GET', 'POST'] )
def conti():
    return render_template( 
                'conti.html'
            )
    
@app.route( '/character', methods = ['GET', 'POST'] )
def character():
    return render_template( 
                'character.html'
            )

@app.route( '/concept', methods = ['GET', 'POST'] )
def concept():
    return render_template( 
                'concept.html'
            )

@app.route( '/ppt', methods = ['GET', 'POST'] )
def ppt():
    return render_template( 
                'ppt.html'
            )

@app.route( '/budget', methods = ['GET', 'POST'] )
def budget():
    return render_template( 
                'budget.html'
            )

@app.route( '/schedule', methods = ['GET', 'POST'] )
def schedule():
    return render_template( 
                'schedule.html'
            )

@app.route( '/pdf', methods=[ 'GET', 'POST' ])
def pdf_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            logging.error('No File in the request')
            return redirect(request.url)
    
        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            logging.error('No Selected File')
            return redirect(request.url)
        
        if uploaded_file and uploaded_file.filename.endswith('.pdf'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filepath)
            logging.info(f'Save Uploaded file to {filepath}')

            pdf_ai = core.PreprodAI()
            logging.info('Start to make SCENE List from PDF')
            results = pdf_ai.find_location_from_pdf(filepath)
            final_results = pprint.pformat(results, indent=4)
            logging.info('Success to make SCENE List from PDF')

            return render_template('pdf.html', result=final_results)

    return render_template('pdf.html')


if __name__ == '__main__':
    app.run( host = '0.0.0.0', debug = 1, port = 5052, threaded = True  )
