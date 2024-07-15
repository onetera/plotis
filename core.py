# :coding: utf-8


import yaml

def main():
    with open( './config.yaml'  ) as f:
        conf = yaml.load( f, load = yaml.FullLoader )
    api_key = conf['api_key']
    return api_key


if __name__ == '__main__':
    print( main() )
