
import pymupdf4llm
import ast
import re
import os
from difflib import SequenceMatcher

def read_scene( file_path ):
    file_name = os.path.basename(file_path)
    if 'pdf' in file_name:
        tmp_scenario = pymupdf4llm.to_markdown( file_path, page_chunks=True )

        scenario = ''
        for s in tmp_scenario:
            tmp_s = s['text'].strip().split('\n')

            edit_scenario = [t for t in tmp_s if not re.fullmatch(r'[^\w\s]*|\d+', t)]

            scenario += '\n\n'.join(edit_scenario)
            scenario += '\n\n'

    elif 'txt' in file_name:
        with open(file_path, 'r') as f:
            scenario = f.read()

    return scenario

def div_scene( chain_method, scenario, div_num ):
    prompt = "아래 시나리오 텍스트를 읽고, 장소나 시간이 전환되는 부분마다 장면을 나누어 무조건 중첩 리스트 형식으로 출력하라."
    prompt += "각 장면은 텍스트에서 시간 또는 장소가 변경될 때 새로운 리스트 항목으로 시작한다."
    prompt += "'CUT TO'와 같은 용어가 포함된 경우, 절대로 장면을 분리하지 말고 반드시 기존 장면의 일부로 취급하라."
    prompt += "각 리스트 항목은 다음과 같이 구성된다 : [숫자(무조건 1), 해당 장면의 전체 텍스트]."
    prompt += "텍스트에 등장하는 모든 표현과 형식(줄 바꿈 포함)을 존중하여 그대로 포함하라."
    prompt += "텍스트의 불완전성 여부에 관계없이, 모든 표현과 문장은 있는 그대로 정확히 포함하라."
    prompt += "각 장면 텍스트의 첫 부분에 포함된 번호, 시간, 장소 등을 반드시 기록하라."
    prompt += "\n"
    prompt += "불필요한 언어 태그나 포맷팅 태그는 절대 포함하지 말고, 반드시 순수한 텍스트 형식의 중첩 리스트만 출력할 것."
    prompt += "\n\n"
    prompt += "시나리오:\n"
    prompt += "{scenario}"

    total_scen_len = len(scenario)
    part_scen_len = total_scen_len // div_num
    last_scen_len = total_scen_len % div_num

    final_res = []

    for p in range(part_scen_len + 1):
        tmp_res = []

        if p == 0:
            chain = chain_method( prompt )
            scenes = chain.invoke( {'scenario':scenario[ : div_num + 100 ]} )
        
        elif p == part_scen_len and last_scen_len == 0:
            scenes="[[1, ' ']]"

        else:
            chain = chain_method( prompt )

            if p != part_scen_len:        
                scenes = chain.invoke( {'scenario':scenario[ p*div_num - 100 : (p+1)*div_num + 100 ]} )

            elif p == part_scen_len and last_scen_len != 0:
                scenes = chain.invoke( {'scenario':scenario[ p*div_num - 100 : ]} )

        tmp_scenes = scenes.replace('```', '').replace('plaintext', '').strip()
        if tmp_scenes.count('[') > tmp_scenes.count(']'):
            tmp_scenes += ']'
        elif tmp_scenes.count('[') < tmp_scenes.count(']'):
            tmp_scenes = tmp_scenes[:-1]

        print('div_scene :: ', tmp_scenes)

        tmp_res.extend(ast.literal_eval(tmp_scenes))

        if len(tmp_res[0][1]) > 1:
            merge_text(final_res, tmp_res)
    
    return final_res

def merge_text(final_res, tmp_res, count=0):
    if len(final_res) == 0:
        for r in tmp_res:
            r[0] += len(final_res) + count
            count += 1
        final_res.extend(tmp_res)
        return final_res
    
    for i, tmp in enumerate(tmp_res):
        match = find_longest_match_text(final_res[-1][1], tmp[1])
        
        if match['size'] > 0 and (match['b'] == 0 or match['a'] + match['size'] == len(final_res[-1][1])):
            merged_text = final_res[-1][1] + tmp[1][match['b'] + match['size']:]
            final_res[-1][1] = merged_text

            for r in tmp_res[i+1:]:
                r[0] += len(final_res) + count
                count += 1
            final_res.extend(tmp_res[i+1:])
            return final_res

    return final_res

def find_longest_match_text(a, b):
    max_match = {'a': 0, 'b': 0, 'size': 0}
    
    for i in range(len(a)):
        matcher = SequenceMatcher(None, a[i:], b)
        match = matcher.find_longest_match(0, len(a) - i, 0, len(b))
        
        if match.size > max_match['size']:
            max_match = {'a': i + match.a, 'b': match.b, 'size': match.size}
    
    return max_match