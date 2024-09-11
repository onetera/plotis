from core import Core

class Conti( Core ):
    def draw_conti( self, scenario, scenario_idx ):
        scene_pattern = re.compile(r'\#\#\# 장면 \d+:')

        scenes = scene_pattern.split(scenario)
        scene_titles = scene_pattern.findall(scenario)

        scene_list = [f"{title.strip()} {scene.strip()}" for title, scene in zip(scene_titles, scenes[1:])]

        prompt_ori = '이 시스템은 영화 콘티작가 입니다.다음 시나리오 일부를 실사 이미지화 해주세요.'
        prompt_ori += "다음에 오는 내용에서 중요 장면 1개를 선정한 후 반드시 아래의 스타일에 맞춰 그려주세요"
        prompt_ori += "만약 컨텐츠 정책이 위반되었다면 반드시 정책을 준수해서 다시 장면 선정을 한 후 이미지를 재생성해주세요."
        prompt_ori += "스타일 : 흑색의 크로키 스타일 스케치, 본질과 감정을 담아낸 부드럽고 표현적인 선, 간결한 배경, 자연스러운 느낌"

        load_conti = self.db.load_conti( scenario_idx )

        for data in scene_list:
            prompt = prompt_ori

            prompt += f"내용 : {data}"
            prompt += "만약 컨텐츠 정책이 위반되었다면 반드시 정책을 준수할 때까지 다시 장면을 선정해서 이미지를 재생성해주세요."

            response = self.oai_client.images.generate(
                model = 'dall-e-3',
                prompt = prompt,
                n = 1,
                size = '1024x1024',
                quality = 'standard',
                style = 'natural'
            )
            image_url = response.data[0].url
            image_url_get = requests.get(image_url)

            img_uid = str(shortuuid.uuid())
            img_path = f'./tmp/conti/{ img_uid }.png'
            with open( img_path, 'wb' ) as f:
                f.write( image_url_get.content )
            
            if not load_conti:
                self.db.insert_conti( data, img_path, scenario_idx )
            else:
                self.db.update_conti( data, img_path, scenario_idx )
            
    def save_conti( self, scenario_idx ):
        wb = Workbook()
        ws = wb.active

        contis = self.db.load_conti( scenario_idx )

        for row, conti_data in enumerate( contis ):
            scene = conti_data[1]
            img_path = conti_data[2]

            cell = ws.cell( row = row+1, column = 1 , value = scene )
            cell.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')

            with open(img_path, 'rb') as img_file:
                img = Image(BytesIO(img_file.read()))
            img.height = 320
            img.width = 320
            ws.add_image( img, 'B{}'.format( row + 1 ) )
            ws.row_dimensions[ row+1 ].height = 320
            ws.column_dimensions[ 'A' ].width = 90

        conti_path = './tmp/conti.xlsx'
        wb.save(  conti_path )
        return conti_path
