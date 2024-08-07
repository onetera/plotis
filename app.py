# :coding: utf-8

from flask import Flask, render_template, request, redirect, session
from flask_session import Session

import os
import pickle

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
        keywords = request.form.get( 'synopsis', '' )

        if not keywords:
            logging.error( 'No Keywords' )
            return redirect( request.url )
        
        preprod_ai = core.PreprodAI()
        logging.info( 'Start to make synopsis list from keywords' )
        preprod_ai.create_synop(keywords)
        #keyword_ai.create_location()
        #keyword_ai.write_scene()
        #logging.info('Start to make synopsis list from keywords')
        
        with open( './synop.txt' , 'w' ) as f:
            f.write( preprod_ai.synop )

        return render_template( 'synopsis.html', synopsis_result= preprod_ai.synop  )

    return render_template( 'synopsis.html' )

@app.route( '/scenario', methods = ['GET', 'POST'] )
def scenario():
    preprod_ai = core.PreprodAI()

    with open( './synop.txt'  ) as f:
        preprod_ai.synop = f.read( )

    if os.path.exists( './location.txt' ):
        with open( './location.txt' ) as f:
            loc_data = f.read()
        preprod_ai.loc = list( loc_data )                    
        logging.info( 'location file exists' )
    else:
        logging.info( 'location file does not exists' )
        preprod_ai.create_location()

    preprod_ai.write_scene()


    return render_template( 'scenario.html', scnario_result = preprod_ai.scenario )
        


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

            pdf_ai = core.PreprodAI_PDF()
            logging.info('Start to make SCENE List from PDF')
            results = pdf_ai.find_location_from_pdf(filepath)
            final_results = pprint.pformat(results, indent=4)
            logging.info('Success to make SCENE List from PDF')

            return render_template('pdf.html', result=final_results)

    return render_template('pdf.html')


if __name__ == '__main__':
    app.run( host = '0.0.0.0', debug = 1, port = 5052, threaded = True  )
