import json
import os
import subprocess
import threading
from pprint import pprint

import docker
import yaml


handing_event = False


def load_config():
    """加载配置文件"""
    path_search = (
        'config.yaml',
        '/config/config.yaml'
    )

    file_path = list(path for path in path_search if os.path.exists(path))

    if len(file_path) == 0:
        raise '配置文件不存在'

    with open(file_path[0], 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        parse_config(config=config)


def parse_config(config: json):
    """解析配置文件"""
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
    """绑定事件"""

    global handing_event

    client = docker.from_env()
    events = client.events(filters={"container": names}, decode=True)
    try:
        for event in events:
            # 检查是否正在处理事件，如果是，则跳过后续事件处理
            if handing_event:
                print('事件处理中，跳过...')
                continue
            thread = threading.Thread(target=handle_event, args=(event, names, valid_events))
            thread.start()
    except KeyboardInterrupt:
        print('程序已停止')


def handle_event(event, names, valid_events):
    """处理事件"""
    print(f'事件：{event}')

    global handing_event

    name = event['Actor']['Attributes']['name']
    if name in names:

        event_model = valid_events[name]

        if event['status'] in list(event_model.keys()):
            print('捕获事件：', name, event.get('status'), event_model[event["status"]])
            handing_event = True
            subprocess.run(f'chmod 777 {event_model[event["status"]]}', shell=True)
            subprocess.run(f'sh {event_model[event["status"]]}', shell=True)
            handing_event = False
