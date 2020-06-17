''' Модуль для работы с API  Trello '''

import requests
import sys


#необходимо добавить свои данные для авторизации(ключ и токен)
auth_params = {
    'key': '',
    'token': '',
}

base_url = "https://api.trello.com/1/{}"

board_id = ""  # вставьте  id доски

def get_data():
    #получает данные доски

    column_data = requests.get(base_url.format('boards')+'/'+board_id+'/lists', params=auth_params).json()
    return column_data

def read():
    #выводит колонки со списком задач

    #получаем данные доски
    column_data = get_data()

    for column in column_data:

        task_data = requests.get(base_url.format('lists')+'/'+column['id']+'/cards', params=auth_params).json()
        print(column['name'], len(task_data))
        if not task_data:
            print('\t' + 'There are not tasks!')
            continue
        for task in task_data:
            print('\t' + task['name'])


def create(name, column_name):
    #создает новое задание

    #получаем данные доски
    column_data = get_data()

    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

def move(name, column_name):
    #перемещает задачи между списками
    column_data = get_data()

    columns = {} #словарь для хранения название_колонки:  id
    tasks = [] #создаем список для заданий
    num_tasks = {} #словарь для хранения номер_задачи: задача
    column_id = None

    for column in column_data:

        columns[column['id']] = column['name'] #добавляем задачи с одинаковым названием в список

        #сохраняем айди требуемой колонки
        if column['name'] == column_name:
            column_id = column['id'] 

        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()

        #добавляем задачи с одинаковым названием в список
        for task in column_tasks:
            if task['name'] == name:
                tasks.append(task)

    #добавляем задания в нумерованный словарь
    for i, task in enumerate(tasks, 1):
        num_tasks[i] = task
    
    
    task_id = None

    #выводим список с одинаковыми названиями          
    for k,v in num_tasks.items():
        print(k, "id-{} task-{} column-{}".format(v['id'], v['name'], columns[v['idList']]))

    #просим пользователя ввести номер необходимой задачи
    _id = int(input('введите номер задачи: '))

    task_id = num_tasks[_id]['id']
    
    requests.put(base_url.format('cards') + '/' + task_id, data={'idList': column_id, **auth_params})
  

def add_list(name):
    #создаем новый список задач

    requests.post(base_url.format('boards')+'/'+board_id + '/'+ '/lists', data={'name': name, **auth_params})


if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'add_list':
        add_list(sys.argv[2])