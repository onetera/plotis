
import pprint
import openai 
from pprint import pprint
import os
import yaml


with open( './config.yml' ) as f:
    data = yaml.load( f, Loader = yaml.FullLoader )
    api_key = data['api_key'] 



def create_synop( *key ):    
    client = openai.OpenAI( api_key = api_key )
    key_list = key
    key_join = ','.join( key_list  )
    search_msg = '''
    {} 시놉시스를 다른내용은 빼고 줄거리만 작성해줘
    '''.format( key_join )
    response = client.chat.completions.create( 
        # model = 'gpt-4-vision-preview',
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




if __name__ == '__main__':
    print( create_synop( '미치광이 과학자','천재과학자' , '코믹', '잔혹' ) )

