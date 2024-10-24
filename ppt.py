# :coding: utf-8

import re
from core import Core
from db_conn import DBconn
from synop import Synop

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN


class PPT( Core ):
    def write_ppt( self, scenario, scenario_idx ):
        search_msg  = '이 시스템은 영화 마케팅 전문가 입니다.'
        search_msg += '아래는 제작을 하려고 하는 시나리오 입니다'
        search_msg += '{body}'
        search_msg += '해당 시나리오를 바탕으로 제작한 영화에 투자자들의 투자를 결정할 수 있는'
        search_msg += '프레젠테이션 파일에 들어갈 슬라이드의 내용들은 아래와 같다'
        search_msg += '['
        search_msg += '영화 소개 : [ 제목, 캐치프레이즈, 장르, 예상 러닝타임, 타겟목표 관객층, 예상 관람등급 등 ]'
        search_msg += '기획의도 : [ ],'
        search_msg += '시놉시스 : [ ],'
        search_msg += '관전포인트 : [ ],'
        search_msg += '캐릭터 소개 : [ 나이, 직업, 성격, 특징 등 ], '
        search_msg += ']'
        search_msg += '이 내용들중 다른 키워드는 작성 하지 말고 반드시 아래의 형식을 따라서 작성해줘'
        search_msg += '기획의도, 관전포인트, 캐릭터 소개는 반드시 감성적 서술체를 바탕으로 서정적인 표현과 비유를 활용해 작성해주세요'
        search_msg += '기획의도는 900~1000자로 서술해주세요.'
        search_msg += '관전포인트는 4가지 이상 번호로 구분해 관객의 감정에 직접적으로 호소해서 각 번호당 300~400자로 서술해주세요'
        search_msg += '주요 캐릭터는 5명 이상 번호로 구분해 등장인물의 성격이 드러난 대사를 활용해 각 번호당 400~500자로 작성해주세요.'
        search_msg += '작성형식)### [슬라이드 1: 영화 소개]'
        search_msg += '- 제목: 영화 제목'
        search_msg += '### [슬라이드 2: 기획의도]'
        search_msg += '기획의도의 내용'
        search_msg += '### [슬라이드 3: 시놉시스]'
        search_msg += '시놉시스의 내용'
        search_msg += '### [슬라이드 4: 관전포인트]'
        search_msg += '1. 첫번째 관전포인트 내용의 명사형'
        
        chain = self.chain( search_msg )
        
        texts = chain.invoke( {'body':scenario} )

        texts_dic = self.parse_ppt(texts)

        ppt_path = self.make_ppt_file(texts_dic, scenario, scenario_idx)

        return ppt_path
    
    def parse_ppt(self, texts):
        title_pattern = re.compile(r'\#\#\# \[슬라이드 \d+: (.*?)\]')
        content_pattern = re.compile(r'\]\n*(.*?)(?:\#\#\#|\Z)', re.DOTALL)

        title_lists = title_pattern.findall(texts)

        texts_dic = {}

        for i in range(len(title_lists)):
            if i != len(title_lists)-1:
                text_tmp = re.search(title_lists[i+1], texts)
                text = texts[:(text_tmp.end()+1)]

                content_lists = content_pattern.findall(text)

                texts = texts[text_tmp.end():]
            else:
                content_lists = content_pattern.findall(texts)

            texts_dic[title_lists[i]] = content_lists[0].strip()
        
        return texts_dic
    
    def make_ppt_file(self, texts_dic, scenario, scenario_idx):
        prs = Presentation( './tmp/template.pptx' )

        template = prs.slides[0]

        for i, (slide_title, slide_content) in enumerate(texts_dic.items()):
            if i < len(prs.slides):
                slide = prs.slides[i]
            else:
                slide_layout = template.slide_layout
                slide = prs.slides.add_slide(slide_layout)

                template_title_shape = template.shapes.title
                title_shape = slide.shapes.title
                self.title_format(template_title_shape, title_shape)

            title = slide.shapes.title
            title.text = slide_title

            left = title.left
            top = title.top + title.height + Inches(0.2)
            width = Inches(9) 
            height = Inches(4) 

            textbox = slide.shapes.add_textbox(left, top, width, height)
            text_frame = textbox.text_frame
            text_frame.word_wrap = True

            if slide_title == '시놉시스':
                if scenario_idx != -1:
                    p = text_frame.add_paragraph()
                    p.text = self.db.last_synop()[0][1] 
                    p.font.size = Pt(14) 
                    p.alignment = PP_ALIGN.LEFT
                else:
                    p = text_frame.add_paragraph()
                    synop = Synop()
                    p.text = synop.analyze_synop(scenario)
                    p.font.size = Pt(14) 
                    p.alignment = PP_ALIGN.LEFT
            
            else:
                sub_content = slide_content.replace('**', '').split('\n')

                for k in sub_content:
                    p = text_frame.add_paragraph()
                    p.text = k.strip()
                    p.font.size = Pt(14) 
                    p.alignment = PP_ALIGN.LEFT

        ppt_path = './tmp/proposal.pptx'
        prs.save(ppt_path)
        
        return ppt_path

    def title_format(self, template_shape, new_shape):
        new_shape.left = template_shape.left
        new_shape.top = template_shape.top
        new_shape.width = template_shape.width
        new_shape.height = template_shape.height
