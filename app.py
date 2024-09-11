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

#import core
import main 
import importlib
importlib.reload( main )

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
        
        preprod_ai = main.PreprodAI()

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
    preprod_ai = main.PreprodAI()

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
                                scenario_result = scenario
                            )
        
@app.route( '/conti', methods = ['GET', 'POST'] )
def conti():
    if request.method == 'POST':
        preprod_ai = main.PreprodAI()

        preprod_ai.scenario = session.get('scenario', '')
        scenario_idx = session.get('scenario_idx', '')
        
        load_scenario = request.form.get( 'load_scenario'   , '' )
        conti = request.form.get( 'conti', '')
        load_conti = request.form.get( 'load_conti', '')
        save_conti = request.form.get( 'save_conti', '')

        if load_scenario:
            scenario = db.last_scenario()
            scenario_result = scenario[0][1]
            scenario_idx = scenario[0][0]
            
            session['scenario'] = scenario_result
            session['scenario_idx'] = scenario_idx
            scenario_result = markdown.markdown( scenario_result )

            return render_template( 'conti.html', scenario_result=scenario_result )
            
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
    if request.method == 'POST':
        preprod_ai = main.PreprodAI()

        preprod_ai.scenario = session.get('scenario', '')
        scenario_idx = session.get('scenario_idx', '')
        
        load_scenario = request.form.get( 'load_scenario'   , '' )
        character = request.form.get( 'character'   , '' )
        load_character = request.form.get( 'load_character'   , '' )

        if load_scenario:
            scenario = db.last_scenario()
            scenario_result = scenario[0][1]
            scenario_idx = scenario[0][0]

            session['scenario'] = scenario_result
            session['scenario_idx'] = scenario_idx
            scenario_result = markdown.markdown( scenario_result )

            return render_template( 'character.html', scenario_result=scenario_result )
        
        elif character:
            character_result = preprod_ai.dev_character( preprod_ai.scenario, scenario_idx )

        
        elif load_character:
            load_character_result = db.load_character( scenario_idx )
            character_result = load_character_result[0][1]


        else:
            return redirect( request.url )
        
        preprod_ai.scenario = markdown.markdown( preprod_ai.scenario )
        character_result = markdown.markdown( character_result )
            
        return render_template( 'character.html', scenario_result=preprod_ai.scenario, character_result=character_result )
    
    return render_template( 'character.html' )

@app.route( '/concept', methods = ['GET', 'POST'] )
def concept():
    if request.method == 'POST':
        preprod_ai = main.PreprodAI()
        preprod_ai.synop     = session.get('synop'     , '')
        preprod_ai.synop_idx = session.get('synop_idx' , '')

        load_synop   = request.form.get( 'load_synop'   , '' )
        concept_img  = request.form.get( 'concept_img'  , '' )
        load_concept = request.form.get( 'load_concept' , '' )

        image_data = ''
        
        if load_synop:
            last_synop       = db.last_synop()
            preprod_ai.synop = last_synop[0][1]
            session['synop'] = preprod_ai.synop
            session['synop_idx'] = preprod_ai.synop

        elif load_concept:
            result = db.load_concept(  preprod_ai.synop_idx )
            if result :
                img_path = result[0][1]
                if os.path.exists( img_path ):
                    with open(img_path, "rb") as img_file:
                        encoded_img = base64.b64encode(img_file.read()).decode('utf-8')
                        image_data = f"data:image/png;base64,{encoded_img}"

        elif concept:
            img_path = preprod_ai.drawing_concept(  preprod_ai.synop )
            db.insert_concept( img_path, preprod_ai.synop_idx ) 

            if os.path.exists( img_path ):
                with open(img_path, "rb") as img_file:
                    encoded_img = base64.b64encode(img_file.read()).decode('utf-8')
                    image_data = f"data:image/png;base64,{encoded_img}"

        return render_template( 
                        'concept.html', 
                        synop_result=preprod_ai.synop ,
                        concept_img = image_data
        )
    return  render_template( 'concept.html' )           


@app.route( '/ppt', methods = ['GET', 'POST'] )
def ppt():
    return render_template( 
                'ppt.html'
            )

@app.route( '/budget', methods = ['GET', 'POST'] )
def budget():
    if request.method == 'POST':
        preprod_ai = main.PreprodAI()

        preprod_ai.scenario = session.get('scenario', '')
        scenario_idx = session.get('scenario_idx', '')
        
        load_scenario = request.form.get( 'load_scenario'   , '' )
        budget = request.form.get( 'budget'   , '' )
        load_budget = request.form.get( 'load_budget'   , '' )

        if load_scenario:
            scenario = db.last_scenario()
            scenario_result = scenario[0][1]
            scenario_idx = scenario[0][0]

            session['scenario'] = scenario_result
            session['scenario_idx'] = scenario_idx
            scenario_result = markdown.markdown( scenario_result )

            return render_template( 'budget.html', scenario_result=scenario_result )
        
        elif budget:
            schedule = db.load_schedule( scenario_idx )
            budget_result = preprod_ai.set_budget( schedule, scenario_idx )

        elif load_budget:
            load_budget_result = db.load_budget( scenario_idx )
            budget_result = load_budget_result[0][1]

        else:
            return redirect( request.url )
        
        preprod_ai.scenario = markdown.markdown( preprod_ai.scenario )
        budget_result = markdown.markdown( budget_result, extensions=['tables'] )
            
        return render_template( 'budget.html', scenario_result=preprod_ai.scenario, budget_result=budget_result )

    return render_template( 'budget.html' )

@app.route( '/schedule', methods = ['GET', 'POST'] )
def schedule():
    if request.method == 'POST':
        preprod_ai = main.PreprodAI()

        preprod_ai.scenario = session.get('scenario', '')
        scenario_idx = session.get('scenario_idx', '')
        
        load_scenario = request.form.get( 'load_scenario'   , '' )
        schedule = request.form.get( 'schedule'   , '' )
        load_schedule = request.form.get( 'load_schedule'   , '' )

        if load_scenario:
            scenario = db.last_scenario()
            scenario_result = scenario[0][1]
            scenario_idx = scenario[0][0]

            session['scenario'] = scenario_result
            session['scenario_idx'] = scenario_idx
            scenario_result = markdown.markdown( scenario_result )

            return render_template( 'schedule.html', scenario_result=scenario_result )
        
        elif schedule:
            schedule_result = preprod_ai.make_schedule( preprod_ai.scenario, scenario_idx )

        
        elif load_schedule:
            load_schedule_result = db.load_schedule( scenario_idx )
            schedule_result = load_schedule_result[0][1]
            pass


        else:
            return redirect( request.url )
        
        preprod_ai.scenario = markdown.markdown( preprod_ai.scenario )
        schedule_result = markdown.markdown( schedule_result )
            
        return render_template( 'schedule.html', scenario_result=preprod_ai.scenario, schedule_result=schedule_result )
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

            pdf_ai = main.PreprodAI()
            logging.info('Start to make SCENE List from PDF')
            results = pdf_ai.find_location_from_pdf(filepath)
            final_results = pprint.pformat(results, indent=4)
            logging.info('Success to make SCENE List from PDF')

            return render_template('pdf.html', result=final_results)

    return render_template('pdf.html')


if __name__ == '__main__':
    app.run( host = '0.0.0.0', debug = 1, port = 5052, threaded = True  )
