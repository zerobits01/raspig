import configparser
import uuid

language = 'en'

server_addr = "http://127.0.0.1"
server_port = 8000

conf = configparser.ConfigParser()

conf.read('pig.conf')

if 'pig' in conf and 'uuid' in conf['pig']:
    pig_uuid = conf['pig']['uuid']
else:
    pig_uuid = uuid.uuid4()
    conf['pig'] = {}
    conf['pig']['uuid'] = str(pig_uuid)
    with open('pig.conf', 'w+') as f:
        conf.write(f)
