from core import Core

class Scenario( Core ):
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
        search_msg += '장면번호는 숫자만 , 장소, 간단한 설명의 순서로 컴마로 구분된  텍스트 형태 데이이터로 만들어줘'
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
        return self.loc

    def create_character( self, synop='' ):
        if synop:
            synop = synop
        else:
            if self.synop:
                synop = self.synop
            else:
                return
        
        search_msg = '{synop}'
        search_msg += '이 시스템은 한국 영화 시나리오 작가이다'
        search_msg += '이 시놉시스를 이용 해서 주요 캐릭터의 이름을 정해줘'
        search_msg += '캐릭터 설명 등 아무것도 출력하지 말고 오직 캐릭터 이름을 컴마로 구분된 텍스트를 담은 리스트형태로 출력해줘.'

        chain = self.chain( search_msg )
        response = chain.invoke( 
                        {'synop':synop  } 
        )
        
        return response
    
    def write_scene( self, loc_list, character_list ):
        ## location 기반으로 작성
        synop_idx = self.db.search_synop_idx(self.synop)

        for loc in loc_list:
            print( 'loc : ', loc )
            search_msg =  '이 시스템은 한국 영화 시나리오 작가이다.'
            search_msg += '모든 장면의 주인공들 이름은 {char_name}이다.'
            search_msg += '이 장면의 번호는 {num}이다.'
            search_msg += '이 장면의 장소는 {location}이다.'
            search_msg += '이 장면의 내용은 {desc}이다.'
            search_msg += '이 정보를 이용해서 상세한 시나리오를 작성해줘.'
            search_msg += '작성예시) ### 장면 0: 장소'

            chain = self.chain( search_msg )
            response = chain.invoke( 
                        {   
                            'char_name'     : character_list,
                            'num'           : loc[0],
                            'location'      : loc[1],
                            'desc'          : loc[2],
                        }

            )
            self.scene_list.append( [ loc[1], response] )
            self.scenario += response
            self.scenario += '\n'
        
        self.db.insert_scenario(self.scenario, synop_idx)

        return self.scenario





