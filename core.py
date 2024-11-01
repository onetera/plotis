
import yaml
import openai
import db_conn

from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import pymupdf4llm
import ast
import re

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
    
    def div_scene( self, pdf_path, div_num ):
        prompt  = "다음 시나리오를 장소 전환을 기준으로 장면을 분리한다."
        prompt += "장소나 시간이 전환됐을 때 반드시 장면구분을 한다."
        prompt += "장소가 전환될 때마다 새롭게 장면을 분리하며, 장소의 세부 위치도 반영한다."
        prompt += "'CUT TO'와 같은 용어가 나왔을 때는 절대 장면구분을 하지 않는다."
        prompt += "전체 시나리오를 수정하거나 요약하지 않고 무조건 그대로 표시한다."
        prompt += "번호(숫자), 장면시나리오 순서로 컴마로 구분된 중첩 리스트 형태 데이터로만 출력한다."
        prompt += "첫번째 리스트 데이터의 번호는 장소나 시간을 알 수 없으면 반드시 0부터, 알 수 있다면 반드시 1로 한다."
        prompt += "그 이후 모든 번호는 첫 번째 번호 데이터를 기준으로 무조건 오름차순으로 매긴다."
        prompt += "데이터 형식 이름 등 다른건 아무것도 출력하지 말고 오직 중첩 리스트만 출력한다."
        prompt += "시나리오 : {scenario}"

        scenario = pymupdf4llm.to_markdown( pdf_path, page_chunks=True )

        total_scen_len = len(scenario)
        part_scen_len = total_scen_len // div_num
        last_scen_len = total_scen_len % div_num

        final_res = []

        for p in range(part_scen_len + 1):
            scenario_text=''
            tmp_res = []
            
            if p != part_scen_len:
                for s in scenario[ p*div_num : (p+1)*div_num ]:
                    tmp_scenario = s['text'].strip().split('\n')

                    edit_scenario = [t for t in tmp_scenario if not re.fullmatch(r'[^\w\s]*|\d+', t)]

                    scenario_text += '\n'.join(edit_scenario)

                chain = self.chain( prompt )                
                scenes = chain.invoke( {'scenario':scenario_text} )

            elif p == part_scen_len and last_scen_len != 0:
                for s in scenario[ p*div_num : ]:
                    tmp_scenario = s['text'].strip().split('\n')

                    edit_scenario = [t for t in tmp_scenario if not re.fullmatch(r'[^\w\s]*|\d+', t)]

                    scenario_text += '\n'.join(edit_scenario)

                chain = self.chain( prompt )                
                scenes = chain.invoke( {'scenario':scenario_text} )
            
            else:
                scenes="[[0, ' ']]"

            tmp_res.extend(ast.literal_eval(scenes.replace('```', '').replace('plaintext', '').replace('json', '').strip()))

            if len(tmp_res[0][1]) > 1:
                if int(tmp_res[0][0]) == 0:
                    if len(final_res):
                        final_res[-1][1] += tmp_res[0][1]

                    for r in tmp_res[1:]:
                        r[0] += len(final_res)
                    final_res.extend(tmp_res[1:])
                elif int(tmp_res[0][0]) == 1:
                    for r in tmp_res:
                        r[0] += len(final_res)
                    final_res.extend(tmp_res)

            print(tmp_res)
        
        return final_res