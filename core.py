
import yaml
import openai
import db_conn

from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import json
import time

class Core( object ):
    
    def __init__( self ):
        with open( './config.yml' ) as f:
            data = yaml.load( f, Loader = yaml.FullLoader )
            self.api_key = data['api_key']

        self.oai_client = openai.OpenAI( 
                                    api_key = self.api_key ,
                                    #**params,
        )

        self.sys_temp = SystemMessagePromptTemplate.from_template(
                    ' 이 시스템은 한국 영화 시나리오 작가이다. 이 시스템은 콘텐츠 정책을 준수 한다.'
        )
        self.db = db_conn.DBconn()

        self.synop = ''
        self.scene_list = []
        self.synopsis = ''
        self.scenario = ''

    def client(self, temperature):
        return ChatOpenAI(
                    model = 'gpt-4o',
                    # model = 'gpt-4o-mini',
                    api_key = self.api_key,
                    temperature=temperature
        )
    
    def chain( self, search_msg , parser = StrOutputParser() ):
        human_temp = HumanMessagePromptTemplate.from_template( search_msg )
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                self.sys_temp,
                human_temp,
            ]
        )
        chain = chat_prompt|self.client(0.5)| parser
        return chain
    
    def analyze_vfx_shot( self, scene ):
        ass_id = 'asst_Qx0UbV8Tk8niKtFZ3jqkdi26'
        ass = self.oai_client.beta.assistants.retrieve( ass_id )
        th_id = 'thread_vvy3waB0VJ65n58i6F1axgh6'
        thread = self.oai_client.bata.threads.retrieve( th_id )

        scene += '\n위 시나리오 장면에서 VFX가 들어갈 요소를 골라줘'
        message = self.oai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content= scene
        )

        run = self.oai_client.beta.threads.runs.create(
            thread_id    = thread.id,
            assistant_id = ass.id,
            model        = "gpt-4o",
        )

        while run.status == 'queued' or run.status == 'in_progress':
            run = self.oai_client.beta.threads.runs.retrieve(
                    thread_id = thread.id,
                    run_id = run.id,
            )
            time.sleep( 1 )
        
        msg = self.oai_client.beta.threads.messages.list( thread_id = thread.id )
        #pprint( json.loads( msg.model_dump_json() )['data']['content'][0]['text']['value'] )
        result = json.loads( msg.model_dump_json() )['data'][0]['content'][0]['text']['value'] 
        return result
    
