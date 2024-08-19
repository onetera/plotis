# :coding: utf-8

from flask import Flask, render_template, request, redirect, session, send_file
from flask_session import Session
import markdown
from openpyxl import load_workbook
import base64
from io import BytesIO
from PIL import Image as PILImage

import os
import pickle
import ast

import pprint

import core
import importlib
importlib.reload(core)

import logging
logging.basicConfig(level=logging.DEBUG)
import db_conn

app = Flask( __name__ )

app.config['UPLOAD_FOLDER'] = './tmp'
app.config['SESSION_TYPE'] = 'filesystem'  # 세션을 파일 시스템에 저장
Session(app)
db = db_conn.DBconn()


@app.route( '/' )
def main_page():
    return render_template( 'main.html' )

@app.route( '/synopsis', methods=[ 'GET', 'POST' ])
def synopsis():
    if request.method == 'POST':

        keywords   = request.form.get( 'keywords', '' )
        load_synop = request.form.get( 'load_synop', '' )
        
        preprod_ai = core.PreprodAI()

        if load_synop:
            last_synop = db.last_synop()
            preprod_ai.synop = last_synop[0][1]
        else:

            if not keywords:
                logging.error( 'No Keywords' )
                return redirect( request.url )
            
            logging.info( 'Start to make synopsis list from keywords' )
            preprod_ai.create_synop(keywords)
            

        session['synop'] = preprod_ai.synop

        return render_template( 'synopsis.html', synopsis_result= preprod_ai.synop  )

    return render_template( 'synopsis.html' )

@app.route( '/scenario', methods = ['GET', 'POST'] )
def scenario():
    preprod_ai = core.PreprodAI()

    preprod_ai.synop = session.get('synop', '')

    scenario      = request.form.get( 'scenario'        , '' )
    load_scenario = request.form.get( 'load_scenario'   , '' )
    
    if load_scenario:
        synop_idx = db.search_synop_idx(preprod_ai.synop)
        last_scenario = db.load_scenario(synop_idx)
        preprod_ai.scenario = last_scenario[0][0]
    elif scenario:

        if not preprod_ai.synop:
            logging.error( 'No Synop' )
            return redirect( request.url )
        
        logging.info( 'Start to make scenario form synopsis' )
        preprod_ai.create_location()
        preprod_ai.write_scene()
    
    session['scenario'] = preprod_ai.scenario

    scenario = markdown.markdown( preprod_ai.scenario )


    return render_template( 
                                'scenario.html', 
                                synopsis_result=preprod_ai.synop, 
                                #scenario_result=preprod_ai.scenario 
                                scenario_result = scenario
                            )
        
@app.route( '/conti', methods = ['GET', 'POST'] )
def conti():
    if request.method == 'POST':
        preprod_ai = core.PreprodAI()

        preprod_ai.scenario = session.get('scenario', '')
        scenario_idx = db.search_sceanrio_idx( preprod_ai.scenario )
        
        load_scenario = request.form.get( 'load_scenario'   , '' )
        conti = request.form.get( 'conti', '')
        load_conti = request.form.get( 'load_conti', '')
        save_conti = request.form.get( 'save_conti', '')

        if load_scenario:
            scenario = db.last_scenario()[0][1]
            scenario_idx = db.search_sceanrio_idx( scenario )
            
            session['scenario'] = scenario
            scenario = markdown.markdown( scenario )

            return render_template( 'conti.html', scenario_result=scenario )
            
        elif conti:
            preprod_ai.write_conti( preprod_ai.scenario, scenario_idx )
            contis = db.load_conti( scenario_idx )
        
        elif load_conti:
            contis = db.load_conti( scenario_idx )
        
        elif save_conti:
            conti_file = preprod_ai.save_conti( scenario_idx )
            return send_file( conti_file, as_attachment=True)

        else:
            return redirect( request.url )
            
        conti_result = []

        for conti_data in contis:
            scene = conti_data[1]
            img_path = conti_data[2]
            
            scene = markdown.markdown( scene )

            image_data = None
            if os.path.exists( img_path ):
                with open(img_path, "rb") as img_file:
                    encoded_img = base64.b64encode(img_file.read()).decode('utf-8')
                    image_data = f"data:image/png;base64,{encoded_img}"
            
            conti_result.append([ scene, image_data ])
        
        return render_template( 'conti.html', conti_result=conti_result )
    return render_template( 'conti.html' )
    
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
