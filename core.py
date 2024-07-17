# :coding: utf-8

import yaml
import openai

from langchain.llms import OpenAI
from langchain.cschema import HumanMessage


# flask app


class PreprodAI:
    def __init__(self ):
        with open( './config.yml' ) as f:
            data = yaml.load( f, Loader = yaml.FullLoader )
            api_key = data['api_key']
        self.client = openai.OpenAI( api_key = api_key )
        self.synop = ''
        self.loc = None
        
    def combine_scene( self ):
        
        loc = self.create_location( self.synop )
        self.loc = loc.choices[0].message.content


            

    def create_synop( self, *key ):    

        key_list = key
        key_join = ','.join( key_list  )
        search_msg = '''
        {} 시놉시스를 다른내용은 빼고 줄거리만 작성해줘
        '''.format( key_join )
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
            max_tokens = 1000
        )
        self.synop = response.choices[0].message.content
        return response


    def create_location( self, synop ):
        search_msg = synop
        search_msg += '\n 이 시놉시스를 이용 해서 80~120개의 장면을 장면번호, 장소, 간단한 설명을 한국말로 설명된 중첩리스트 데이터로 만들고 출력은 생성된 중첩 데이터 만 출력'
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
            max_tokens = 1000
        )

        return response
        
    def create_scene( self, scene_num ):
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
            max_tokens = 1000
        )

        return resonse
        

        


