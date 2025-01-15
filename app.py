# :coding: utf-8

from flask import Flask, render_template, request, redirect, session, send_file, url_for, send_from_directory, jsonify
from flask_session import Session
import markdown
import base64

import os

import pprint

import main 
import importlib
importlib.reload( main )

import logging
logging.basicConfig(level=logging.DEBUG)
import db_conn

from ctrl_scene import read_scene

app = Flask( __name__ )

app.config['UPLOAD_FOLDER'] = './tmp'
app.config['SESSION_TYPE'] = 'filesystem'  # 세션을 파일 시스템에 저장
Session(app)
db = db_conn.DBconn()

@app.route( '/' )
def main_page():
    login_id = session.get('login_id', '')
    print( '\n' )
    print( 'login_id : ' , login_id )
    return render_template( 'index.html', login_id = login_id )
    # return render_template( 'main.html', login_id = login_id )

@app.route( '/dashboard' )
def dashboard_page():
    login_id = session.get('login_id', '')
    print( '\n' )
    print( 'login_id : ' , login_id )
    return render_template( 'dashboard.html', login_id = login_id )

@app.route( '/aboutus' )
def aboutus_page():
    login_id = session.get('login_id', '')
    print( '\n' )
    print( 'login_id : ' , login_id )
    return render_template( 'aboutus.html', login_id = login_id )

@app.route( '/features' )
def features_page():
    login_id = session.get('login_id', '')
    print( '\n' )
    print( 'login_id : ' , login_id )
    return render_template( 'features.html', login_id = login_id )

@app.route( '/contact' )
def contact_page():
    login_id = session.get('login_id', '')
    print( '\n' )
    print( 'login_id : ' , login_id )
    return render_template( 'contact.html', login_id = login_id )

@app.route( '/previz' )
def previz():
    login_id = session.get('login_id', '')
    print( '\n' )
    print( 'login_id : ' , login_id )
    return render_template( 'previz.html', login_id = login_id )

@app.route( '/loading' )
def loading():
    login_id = session.get('login_id', '')
    print( '\n' )
    print( 'login_id : ' , login_id )
    return render_template( 'loading.html', login_id = login_id )

@app.route( '/login', methods=[ 'GET', 'POST' ] )
def login():
    login_id = request.form.get( 'login_id', '' )
    login_pw = request.form.get( 'login_pw', '' )
    if db.login( login_id, login_pw ):
        session['login_id'] = login_id        
        return redirect( url_for( 'main_page' ) )

    return render_template( 'login.html' )

@app.route( '/logout' )
def logout():
    session.pop( 'login_id' , None )
    return redirect( url_for( 'main_page') )

@app.route( '/<filename>', methods=[ 'GET', 'POST' ] )
def pop_up(filename):
    logging.info(f"Requested popup file : {filename}")
    previous_page = request.referrer
    logging.info(f"Previous page : {previous_page}")

    if 'pop_up.html' in filename:
        popup_data = db.last_5_synop()
        return render_template( filename, popup_data=popup_data )
    
    elif 'pop_up2.html' in filename:
        if '/scenario' in previous_page:
            synop_idx = session.get('synop_idx', None)
            if synop_idx:
                popup_data = db.load_scenario(synop_idx)
                return render_template( filename , popup_data=popup_data )
        else:
            popup_data = db.last_5_scenario()
            return render_template( filename , popup_data=popup_data )

    elif 'pop_up3.html' in filename:
        scen_idx = session.get('scen_idx', None)
        if scen_idx:
            popup_data = []
            div_data = []
            count = 1

            find_div_scenarios = db.load_div_scene(scen_idx)
            for f in find_div_scenarios:
                if f[1] == 1:
                    if div_data:
                        popup_data.append([count, div_data])
                        count += 1
                        div_data.clear()
                content = f[2]
                img_path = db.load_conti(f[0])
                div_data.append([content, img_path])
            
            popup_data.append([count, div_data])

        return render_template( filename, popup_data=popup_data )

    elif 'pop_up4.html' in filename:
        synop_idx = session.get('synop_idx', None)
        synop_content = db.search_synop_using_idx(synop_idx)
        if synop_idx:
            popup_data = db.load_concept(synop_content)
        return render_template( filename, popup_data=popup_data )
    
    elif 'pop_up5.html' in filename:
        scen_idx = session.get('scen_idx', None)
        if scen_idx:
            popup_data = db.load_character(scen_idx)
        return render_template( filename, popup_data=popup_data )

    elif 'pop_up6.html' in filename:
        scen_idx = session.get('scen_idx', None)
        if scen_idx:
            popup_data = db.load_schedule(scen_idx)
            print(popup_data)
            print()
            print(popup_data[0])
        return render_template( filename, popup_data=popup_data )

    elif 'pop_up7.html' in filename:
        scen_idx = session.get('scen_idx', None)
        if scen_idx:
            popup_data = db.load_budget(scen_idx)
        return render_template( filename, popup_data=popup_data )
        
    elif 'pop_up8.html' in filename:
        scen_idx = session.get('scen_idx', None)
        if scen_idx:
            popup_data = db.load_ppt(scen_idx)
        return render_template( filename, popup_data=popup_data )
    
    else:
        return render_template( filename )

@app.route('/load_synop_ajax', methods=['POST'])
def load_synop_ajax():
    session['synop_idx'] = None
    data = request.get_json()
    synop_idx = data.get('synop_idx', None)
    if not synop_idx:
        return jsonify({"success": False})

    session['synop_idx'] = synop_idx

    return jsonify({"success": True})

@app.route('/load_scen_ajax', methods=['POST'])
def load_scen_ajax():
    data = request.get_json()
    scen_idx = data.get('scen_idx', None)   # 시나리오 식별자
    if not scen_idx:
        return jsonify({"success": False})

    session['scen_idx'] = scen_idx

    return jsonify({"success": True})
    # return jsonify({"success": True, "scenario_data": scenario_data})

@app.route( '/check_login' , methods=[ 'GET', 'POST' ] )
def check_login( ):
    login_id = request.form.get( 'login_id', '' )
    login_pw = request.form.get( 'login_pw', '' )
    login_info = db.login( login_id , login_pw )


@app.route( '/synopsis', methods=[ 'GET', 'POST' ])
def synopsis():
    login_id = session.get('login_id', '')
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
            preprod_ai.synop = preprod_ai.write_synop(keywords)
            
        session['synop'] = preprod_ai.synop

        return render_template( 'synopsis.html', synopsis_result= preprod_ai.synop , login_id= login_id )

    return render_template( 'synopsis.html', login_id = login_id )


@app.route( '/scenario', methods = ['GET', 'POST'] )
def scenario():
    login_id = session.get('login_id', '')
    preprod_ai = main.PreprodAI()

    preprod_ai.synop = session.get('synop', '')

    scenario      = request.form.get( 'scenario'        , '' )
    load_scenario = request.form.get( 'load_scenario'   , '' )
    
    if load_scenario:
        synop_idx = db.search_synop_idx(preprod_ai.synop)
        last_scenario = db.load_scenario(synop_idx)
        print(synop_idx)
        print(last_scenario)
        preprod_ai.scenario = last_scenario[0][0]
    elif scenario:

        if not preprod_ai.synop:
            logging.error( 'No Synop' )
            return redirect( request.url )
        
        logging.info( 'Start to make scenario form synopsis' )
        # preprod_ai.create_location()
        preprod_ai.scenario = preprod_ai.write_scene( preprod_ai.synop )
    
    session['scenario'] = preprod_ai.scenario

    scenario = markdown.markdown( preprod_ai.scenario )


    return render_template( 
                                'scenario.html', 
                                synopsis_result = preprod_ai.synop, 
                                scenario_result = scenario,
                                login_id        = login_id
                            )
        
@app.route( '/conti', methods = ['GET', 'POST'] )
def conti():
    login_id = session.get('login_id', '')
    if request.method == 'POST':
        preprod_ai = main.PreprodAI()

        preprod_ai.scenario = session.get('scenario', '')
        scenario_idx = session.get('scenario_idx', '')
        
        load_scenario = request.form.get( 'load_scenario'   , '' )
        upload_scenario     = request.form.get( 'upload_scenario' , '' )
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

            return render_template( 'conti.html', scenario_result=scenario_result , login_id = login_id )
        
        elif upload_scenario:
            file = request.files['select_file'] 
            scenario_path = './tmp/uploaded/' + file.filename 
            os.makedirs(os.path.dirname(scenario_path), exist_ok=True)

            file.save( scenario_path )

            scenario_result = read_scene( scenario_path )
            # db.insert_scenario( scenario_result, None, 0)
            search_scenario_idx = db.search_scenario_idx( scenario_result )
            if not search_scenario_idx:
                scenario_idx = db.insert_scenario( scenario_result, None, 0)
            else:
                scenario_idx = search_scenario_idx[0][0]
            
            session['scenario'] = scenario_result
            session['scenario_idx'] = scenario_idx

            return render_template( "conti.html", uploaded = True , login_id = login_id )

        elif conti:
            preprod_ai.draw_conti( preprod_ai.scenario, scenario_idx )
            scenes = db.load_div_scene( scenario_idx )
        
        elif load_conti:
            scenes = db.load_div_scene( scenario_idx )
        
        elif save_conti:
            conti_file = preprod_ai.save_conti( scenario_idx )
            return send_file( conti_file, as_attachment=True)

        else:
            return redirect( request.url )
            
        conti_result = []

        for scene_data in scenes:
            scene = scene_data[2]
            img_path = db.load_conti( scene_data[0] )
            
            scene = markdown.markdown( scene )

            image_data = None
            if os.path.exists( img_path ):
                with open(img_path, "rb") as img_file:
                    encoded_img = base64.b64encode(img_file.read()).decode('utf-8')
                    image_data = f"data:image/png;base64,{encoded_img}"
            
            conti_result.append([ scene, image_data ])
        
        return render_template( 'conti.html', conti_result=conti_result , login_id = login_id )
    return render_template( 'conti.html' , login_id = login_id )
    
@app.route( '/character', methods = ['GET', 'POST'] )
def character():
    login_id = session.get('login_id', '')
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

            return render_template( 'character.html', scenario_result=scenario_result , login_id = login_id )
        
        elif character:
            character_result = preprod_ai.dev_character( preprod_ai.scenario, scenario_idx )

        
        elif load_character:
            load_character_result = db.load_character( scenario_idx )
            character_result = load_character_result[0][1]


        else:
            return redirect( request.url )
        
        preprod_ai.scenario = markdown.markdown( preprod_ai.scenario )
        character_result = markdown.markdown( character_result )
            
        return render_template( 
                                'character.html', 
                                scenario_result  = preprod_ai.scenario, 
                                character_result = character_result ,
                                login_id = login_id
                                )
    
    return render_template( 'character.html' , login_id = login_id )

@app.route( '/concept', methods = ['GET', 'POST'] )
def concept():
    login_id = session.get('login_id', '')
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
                        synop_result = preprod_ai.synop ,
                        concept_img  = image_data,
                        login_id = login_id 
        )
    return  render_template( 'concept.html', login_id = login_id )           


@app.route( '/ppt', methods = ['GET', 'POST'] )
def ppt():
    login_id = session.get('login_id', '')
    if request.method == 'POST':
        preprod_ai = main.PreprodAI()

        preprod_ai.scenario = session.get('scenario'    , '' )
        scenario_idx        = session.get('scenario_idx', '' )
        load_scenario       = request.form.get( 'load_scenario'   , '' )
        upload_scenario     = request.form.get( 'upload_scenario' , '' )
        download_ppt        = request.form.get( 'download_ppt'    , '' )
        load_ppt            = request.form.get( 'load_ppt'    , '' )

        print( )
        print( upload_scenario )
        print( load_scenario )
        print( )

        if load_scenario:
            scenario        = db.last_scenario()
            scenario_result = scenario[0][1]
            scenario_idx    = scenario[0][0]

            session['scenario']     = scenario_result
            session['scenario_idx'] = scenario_idx
            scenario_result         = markdown.markdown( scenario_result )

            return render_template( 'ppt.html', scenario_result=scenario_result, login_id = login_id )

        elif upload_scenario:
            file = request.files['select_file'] 
            scenario_path = './tmp/uploaded/' + file.filename 
            os.makedirs(os.path.dirname(scenario_path), exist_ok=True)

            file.save( scenario_path )

            scenario_result = read_scene( scenario_path )
            search_scenario = db.search_scenario_idx( scenario_result )
            if not search_scenario:
                scenario_idx = db.insert_scenario( scenario_result, None, 0)
            else:
                scenario_idx = search_scenario[0][0]
                
            session['scenario'] = scenario_result
            session['scenario_idx'] = scenario_idx
            
            return render_template( "ppt.html", uploaded = True , login_id = login_id )

        elif download_ppt:
            print( '+' * 50 )
            print( 'download ppt' )
            if session['scenario']:
                print( '=' * 50 )
                print( 'session' )
                preprod_ai.scenario = session['scenario']
                scenario_idx = session['scenario_idx']
                ppt_path = preprod_ai.write_ppt( preprod_ai.scenario, scenario_idx )
                download_ppt_result = url_for('download_ppt_file', ppt_path=ppt_path)
                print( '^' * 50 )
                print( ppt_path )
                return render_template( "ppt.html", download_ppt_link = download_ppt_result, login_id = login_id )
        
        elif load_ppt:
            scenario_idx = session['scenario_idx']
            ppt_path = db.load_ppt_path( scenario_idx )
            if ppt_path:
                download_ppt_result = url_for('download_ppt_file', ppt_path=ppt_path[0][0])
                return render_template( "ppt.html", download_ppt_link = download_ppt_result, login_id = login_id )
            else:
                return render_template( 'ppt.html' , login_id = login_id )  

    return render_template( 'ppt.html' , login_id = login_id )   

@app.route('/download_ppt')
def download_ppt_file():
    ppt_path = request.args.get('ppt_path')
    if ppt_path and os.path.exists(ppt_path):
        return send_file(ppt_path, as_attachment=True)

@app.route('/tmp/<path:filename>')
def use_tmp_file(filename):
    previous_page = request.referrer
    if '/ppt' in previous_page:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        # return send_from_directory('tmp', filename)
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route( '/budget', methods = ['GET', 'POST'] )
def budget():
    login_id = session.get('login_id', '')
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

            return render_template( 'budget.html', scenario_result=scenario_result, login_id = login_id  )
        
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
            
        return render_template( 
                                'budget.html', 
                                scenario_result = preprod_ai.scenario, 
                                budget_result   = budget_result,
                                login_id = login_id 
                                )

    return render_template( 'budget.html', login_id = login_id )

@app.route( '/schedule', methods = ['GET', 'POST'] )
def schedule():
    login_id = session.get('login_id', '')
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

            return render_template( 'schedule.html', scenario_result = scenario_result, login_id = login_id )
        
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
            
        return render_template( 
                                'schedule.html', 
                                scenario_result = preprod_ai.scenario, 
                                schedule_result = schedule_result ,
                                login_id = login_id
                                )
    return render_template( 
                'schedule.html' , login_id = login_id 
            )

@app.route( '/pdf', methods=[ 'GET', 'POST' ])
def pdf_page():
    login_id = session.get('login_id', '')
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

            return render_template('pdf.html', result = final_results , login_id = login_id )

    return render_template('pdf.html' , login_id = login_id )


if __name__ == '__main__':
    app.run( host = '0.0.0.0', debug = 1, port = 5052, threaded = True  )
