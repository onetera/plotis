# :coding: utf-8

import yaml
import openai

from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate , HumanMessagePromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core import output_parsers 

from openpyxl import Workbook
from openpyxl.drawing.image import Image

import requests
from io import BytesIO




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
        self.scene_list = []
        
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

    def create_location( self, min = 80, max = 120, synop = '' ):
        if synop:
            synop = synop
        else:
            if self.synop:
                synop = self.synop
            else:
                return

        search_msg = '{synop}'
        search_msg += '이 시스템은 한국 영화 시나리오 작가이다'
        search_msg += '이 시놉시스를 이용 해서 기승전결있는  {min}~{max}개의 장면을 만들어줘'
        search_msg += '장면번호는 숫자만 , 장소, 간단한 설명의 순서로 텍스트 형태 데이이터로 만들어줘'
        search_msg += '데이터 형식 이름 같이  다른건 아무것도 출력하지 말고 오직 생성된 중첩 데이터만 출력해줘.'
        search_msg += '장면이 {min}개 이하면 좀더 계산해서 기승전결이 있는 {min}개~{max}개의 장면이 되도록 작성해줘.'

        chain = self.chain( search_msg )
        response = chain.invoke( 
                        {'synop':synop, 'min' : min, 'max':max } 
        )
        loc_list = []
        for row in response.split('\n'):
            loc_list.append( row.split(',') )
        self.loc = loc_list
        return response

    def write_scene( self ):
        ## location 기반으로 작성
        with open('./tmp/scenario.txt' , 'w' ) as f:

            i = 0
            for loc in self.loc:
                print( loc )
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
                f.write( response )              
                self.scene_list.append( [ loc[1], response] )

    def write_conti( self ):
        wb = Workbook()
        ws = wb.active

        i = 0
        for row, data in enumerate( self.scene_list ):
            ws.cell( row = row+1, column = 1 , value = data[-1] )
            prompt = '이 시스템은 영화 콘티작가 입니다.다음 시나리오 일부를 실사 이미지화 해주세요.'
            prompt += '컨텐츠 정책을 준수해서 이미지를 만들어 주세요.'
            prompt += '컨텐츠 정책이 위반 되었다면 다시 정책을 준수 해서 다시 이미지를 만들어 주세요.'
            prompt += data[-1]

            response = self.oai_client.images.generate(
                model = 'dall-e-3',
                prompt = prompt,
                n = 1,
                size = '1024x1024',
            )
            image_url = response.data[0].url
            image_path = requests.get(image_url)
            img = Image( BytesIO(image_path.content) )
            img.height = 320
            img.width = 320
            ws.add_image( img, 'B{}'.format( row + 1 ) )
            ws.row_dimensions[ row+1 ].height = 320
            ws.column_dimensions[ 'A' ].width = 90
        wb.save(   './tmp/conti.xlsx' )
           

        

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

        

        


