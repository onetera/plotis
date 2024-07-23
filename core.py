# :coding: utf-8

import yaml
import openai

from langchain.chat_models import ChatOpenAI
#from langchain.cschema import HumanMessage
from langchain_core.prompts import SystemMessagePromptTemplate , HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
#from langchain_core.output_parsers import StrOutputParser
from langchain_core import output_parsers 


# flask app


class PreprodAI:
    def __init__(self ):
        with open( './config.yml' ) as f:
            data = yaml.load( f, Loader = yaml.FullLoader )
            api_key = data['api_key']
        params = {
                    'temperature' : 0.5,
        }
        
        self.oai_client = openai.OpenAI( 
                                    api_key = api_key ,
                                    #**params,
        )

        self.client = ChatOpenAI(
                    model = 'gpt-4o-mini',
                    api_key = api_key,
                    **params,
        )
        self.sys_temp = SystemMessagePromptTemplate.from_template(
                    ' 이 시스템은 영화 시나리오 작가이다.'
        )

        self.synop = ''
        self.loc = None
        
    def combine_scene( self ):
        loc = self.create_location( self.synop )
        self.loc = loc.choices[0].message.content


    def create_synop( self, *key ):    
        key_list = key
        key_join = ','.join( key_list  )
        search_msg = '{key_join} 이런 내용의 시놉시스를 작성해줘.'
        search_msg += '제목같은 다른 내용은 출력하지 말고 시놉시스의 내용만 출력'
        chain = self.chain( search_msg )
        response = chain.invoke({'key_join':key_join}  )
        self.synop = response
        return response

    def create_location( self, synop = '' ):
        if synop:
            synop = synop
        else:
            if self.synop:
                synop = self.synop
            else:
                return

        search_msg = '{synop}'
        search_msg += '이 시스템은 한국 영화 시나리오 작가이다'
        search_msg += '이 시놉시스를 이용 해서 기승전결있는  80~120개의 장면을 만들어줘'
        search_msg += '장면번호는 숫자만 , 장소, 간단한 설명의 순서로 텍스트 형태 데이이터로 만들어줘'
        #search_msg += '장면번호는 숫자만 , 장소, 간단한 설명의 순서로 json이 아닌 python의 중첩리스트 데이터로 만들어줘'
        search_msg += '데이터 형식 이름 같이  다른건 아무것도 출력하지 말고 오직 생성된 중첩 데이터만 출력해줘.'
        search_msg += '장면이 80개 이하면 좀더 계산해서 기승전결이 있는 80개~120개의 장면이 되도록 작성해줘.'

        chain = self.chain( search_msg )
        response = chain.invoke( {'synop':synop} )
        loc_list = []
        for row in response.split('\n'):
            loc_list.append( row.split(',') )
        self.loc = loc_list
        return response

    def write_scene( self ):
        ## location 기반으로 작성

        i = 0
        for loc in self.loc:
            search_msg =  '이 시스템은 한국 영화 시나리오 작가이다.'
            search_msg += '이 장면의 번호는 {num}이다.'
            search_msg += '이 장면의 장소는 {location}이다.'
            search_msg += '이 장면의 내용은 {desc}이다.'
            search_msg += '이 정보를 이용해서 상세한 시나리오를 작성해줘.'

            chain = self.chain( search_msg )
            response = chain.invoke( 
                        {   
                            'num'     : loc[0],
                            'location': loc[1],
                            'desc'    : loc[2],
                        }

            )
            print( response )
            if i == 4 :
                return
            i += 1       

    def chain( self, search_msg , parser = StrOutputParser() ):
        human_temp = HumanMessagePromptTemplate.from_template( search_msg )
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                self.sys_temp,
                human_temp,
            ]
        )
        chain = chat_prompt|self.client| output_parsers.StrOutputParser()
        return chain

        
    def create_scene( self, scene_num ):
        ## test
        search_msg = '{}번 장면에 대해 상세한 시나리오를 작성해줘'
        response = self.client.chat.completions.create( 
            model = 'gpt-4o',
            messages = [
                {
                    'role' : 'user',
                    'content' : [
                        {'type':'text', 'text' : search_msg },
                    ]
                }
            ],
            #max_tokens = 1000
        )

        return resonse
        
    def create_synop2( self, *key):
        ## test
        key_list = key
        key_join = ','.join( key_list  )

        search_msg = '\n이 시스템은 영화 시나리오 작가이다.'
        search_msg += '{} 등의 키워드를 가진 시놉시스를 작성해줘.'.format( key_join )
        search_msg += '제목같은 다른 내용은 출력하지 말고 시놉시스의 내용만 출력해줘'

        response = self.oai_client.chat.completions.create( 
            model = 'gpt-4o-mini',
            messages = [
                {
                    'role' : 'user',
                    'content' : [
                        {'type':'text', 'text' : search_msg },
                    ]
                }
            ],
            #max_tokens = 1000
        )
        self.synop = response.choices[0].message.content

    def create_location2( self ):
        ## test
        #search_msg = '{}번 장면에 대해 상세한 시나리오를 작성해줘'
        search_msg = '\n이 시스템은 영화 시나리오 작가이다.'
        search_msg +=  self.synop 
        search_msg +=  '.\n'
        search_msg += '이 시놉시스를 이용한 시나리오를 작성해서 50~100개의 장면으로 만들어줘.'
        search_msg += '장면번호, 장소, 간단한 설명을 한국말로 설명된 중첩리스트 데이터로 만들어줘.'
        search_msg += '출력은 다른데이터는 출력하지 말고 중첩 데이터만 출력해줘.'
        search_msg += '장면이 80개 이하면 좀더 계산해서 80개~120개의 장면이 되도록 작성해줘.'

        response = self.oai_client.chat.completions.create( 
            model = 'gpt-4o-mini',
            messages = [
                {
                    'role' : 'user',
                    'content' : [
                        {'type':'text', 'text' : search_msg },
                    ]
                }
            ],
            #max_tokens = 1000
        )

        return response.choices[0].message.content

        


