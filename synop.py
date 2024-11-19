# :coding: utf-8

from core import Core


class Synop( Core ):
    def write(self, *key):
        key_list = list(key)
        key_join = ','.join( key_list  )
        search_msg = '{key_join} 이런 내용의 시놉시스를 작성해줘.'
        search_msg += '제목같은 다른 내용은 출력하지 말고 시놉시스의 내용만 출력'
        search_msg += '900자 ~ 1000자 로 출력하세요'
        chain = self.chain( search_msg )
        response = chain.invoke({'key_join':key_join}  )
        self.synop = response
        self.db.insert_synop( response, key_join )
        return response
    
    def analyze_synop(self, scenario):
        search_msg = '이 시스템은 유명한 시나리오 분석가입니다.'
        search_msg += '아래의 시나리오를 읽고 시놉시스를 작성해주세요.'
        search_msg += '제목같은 다른 내용은 출력하지 말고 시놉시스의 내용만 출력하세요.'
        search_msg += '900자 ~ 1000자 로 출력하세요'
        search_msg += '시나리오 : {scenario}'
        chain = self.chain( search_msg )
        response = chain.invoke({'scenario':scenario})
        return response
        
