
class Core( object ):
    
    def __init__( self ):
        with open( './config.yml' ) as f:
            data = yaml.load( f, Loader = yaml.FullLoader )
            self.api_key = data['api_key']

        self.oai_client = openai.OpenAI( 
                                    api_key = self.api_key ,
                                    #**params,
        )

        self.sys_temp = SystemMessagePromptTemplate.from_template(
                    ' 이 시스템은 한국 영화 시나리오 작가이다. 이 시스템은 콘텐츠 정책을 준수 한다.'
        )
        self.db = db_conn.DBconn()

    def client(self, temperature):
        return ChatOpenAI(
                    model = 'gpt-4o',
                    # model = 'gpt-4o-mini',
                    api_key = self.api_key,
                    temperature=temperature
        )

