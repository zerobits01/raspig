import requests
from configs import server_addr, server_port
from configs import pig_uuid


get_task_url = "/api/pig/pig/?uuid={pig_uuid}"
get_point_url = "/api/pig/point/?uuid={pig_uuid}"
task_update_url = "/api/pig/task-update/{id}/"


def get_new_tasks():
    resp = requests.get(
        f'{server_addr}:{server_port}{get_task_url.format(pig_uuid=pig_uuid)}'
    )
    return resp.json()


def get_point():
    resp = requests.get(
        f'{server_addr}:{server_port}{get_point_url.format(pig_uuid=pig_uuid)}'
    )
    return resp.json()


def update_task_to_done(goal_id: int):
    resp = requests.patch(
        f'{server_addr}:{server_port}{task_update_url.format(id=goal_id)}',
        data={
            'uuid': pig_uuid,
            'goal_id': goal_id
        }
    )
    return resp.json()