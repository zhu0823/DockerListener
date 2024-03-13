import json
import os
import subprocess
from pprint import pprint

import docker
import yaml


def load_config():

    file_path = 'config.yaml'

    if os.getenv('DOCKER_ENV', False):
        file_path = '/config/config.yaml'

    if not os.path.exists(file_path):
        raise '配置文件不存在'

    with open(file_path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        parse_config(config=config)


def parse_config(config: json):
    # 所有容器
    containers = config['containers']

    valid_entity = {}
    for container in containers:
        name: str = container['name']
        events: {str: str} = container['events']

        # 过滤脚本文件存在的事件
        valid_events = {key: value for key, value in events.items() if os.path.exists(value)}

        if len(valid_events) == 0:
            print(f'容器{name}没有有效的事件')
        else:
            valid_entity[name] = valid_events
            pprint(f'有效事件 {name}: {valid_events}')

    bind_event(names=list(valid_entity.keys()), valid_events=valid_entity)


def bind_event(names: [str], valid_events: {}):
    client = docker.from_env()
    events = client.events(filters={"container": names}, decode=True)
    try:
        for event in events:
            print(f'事件：{event}')
            name = event['Actor']['Attributes']['name']
            if name in names:

                event_model = valid_events[name]

                if event['status'] in list(event_model.keys()):
                    print('捕获事件：', name, event.get('status'), event_model[event["status"]])
                    subprocess.run(f'chmod 777 {event_model[event["status"]]}', shell=True)
                    subprocess.run(f'sh {event_model[event["status"]]}', shell=True)
    except KeyboardInterrupt:
        print('程序已停止')


def scripts_path() -> str:
    docker_env = os.getenv('DOCKER_ENV', default=False)

    if docker_env.lower() == 'true':
        return '/app/scripts'
    else:
        return './scripts'
