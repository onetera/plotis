from core import Core


class Schedule( Core ):
    def schedule( self, scenario, scenario_idx ):
        search_msg = '이 시스템은 유능한 넷플릭스 콘텐츠 PM입니다.'
        search_msg += '다음 시나리오를 넷플릭스에서 방영한다고 했을 때 현실적인 넷플릭스 영화 제작 스케줄을 짜주세요.'
        search_msg += '스케줄은 날짜가 아닌 기간으로 작성해야 하며, 영화 제작의 모든 과정이 효율적으로 이루어질 수 있도록 계획해주세요.'
        search_msg += 'Preproduction, Production, Postproduction, P&A 순으로 작성하세요.'
        search_msg += 'Production은 16~20주 이내로 설정해주세요.'
        search_msg += 'Postproduction은 편집은 8주 이내로, 그 외는 16~24주 이내로 설정해주세요.'
        search_msg += '제작 스케줄을 상세하게 짜주세요.'
        search_msg += '상세내용은 반드시 명사로 마무리하고, 문장 형태로 작성하지 마세요.'
        search_msg += '다른 어떠한 추가 문장이나 설명도 출력하지 말고, 반드시 작성 예시를 엄격히 따라 작성하세요.'
        search_msg += '시나리오 : {scenario}'
        search_msg += '작성 예시) ## 1. Preproduction'
        search_msg += '#### 시나리오 개발'
        search_msg += '- 내용: 시나리오 최종 수정 및 확정'
        search_msg += '- 기간: 6주'
        chain = self.chain(search_msg)

        response = chain.invoke( {'scenario':scenario} )

        load_schedule = self.db.load_schedule( scenario_idx )
            
        if not load_schedule:
            self.db.insert_schedule( response, scenario_idx )
        else:
            self.db.update_schedule( response, scenario_idx )
        
        return response