# :coding: utf-8

from flask import Flask, render_template, request, redirect

import os
import pprint

import core
import importlib
importlib.reload(core)

import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask( __name__ )

app.config['UPLOAD_FOLDER'] = './tmp'


@app.route( '/' )
def main_page():
    return render_template( 'main.html' )

@app.route( '/keyword', methods=[ 'GET', 'POST' ])
def keyword_page():
    if request.method == 'POST':
        keywords = request.form.get('keywords', '')

        if not keywords:
            logging.error('No Keywords')
            return redirect(request.url)
        
        keyword_ai = core.PreprodAI()
        logging.info('Start to make SCENE List from Keywords')
        keyword_ai.create_synop(keywords)
        keyword_ai.create_location()
        keyword_ai.write_scene()
        logging.info('Start to make SCENE List from Keywords')

        return render_template( 'keyword.html', result=f'Save Scenario at ./tmp/scenario.txt' )

    return render_template( 'keyword.html' )

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
