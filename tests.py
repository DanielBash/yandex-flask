import requests


def test_get_single_job():
    """Получение одной работы"""
    requests.get('http://localhost:5000/api/jobs/1').json()


def test_get_multiple_jobs():
    """Получение нескольких работ"""
    requests.get('http://localhost:5000/api/jobs').json()


def test_get_single_job_wrong_id():
    """Получение работы с неверным id"""
    requests.get('http://localhost:5000/api/jobs/-1').json()


def test_get_single_job_string_id():
    """Получение работы с неверным id-строкой"""
    requests.get('http://localhost:5000/api/jobs/test_string').json()


def test_add_job():
    """Создание работы"""
    params = {
        "is_finished": False,
        "job": "Develop login system",
        "collaborators": "1, 2",
        "team_leader": 1,
        "work_size": 10,
        "category": 1
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/jobs/add",
        params=params
    ).json()


def test_add_job_wrong_work_size():
    """Неверное созание работы cо сложностью-строкой"""
    params = {
        "is_finished": False,
        "job": "Develop login system",
        "collaborators": "1, 2",
        "team_leader": 1,
        "work_size": "10",
        "category": 1
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/jobs/add",
        params=params
    ).json()


def test_add_job_wrong_team_leader():
    """Неверное созание работы c лидером-строкой"""
    params = {
        "is_finished": False,
        "job": "Develop login system",
        "collaborators": "1, 2",
        "team_leader": "1",
        "work_size": 10,
        "category": 1
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/jobs/add",
        params=params
    ).json()


for i in list(globals()):
    if i.startswith('test_'):
        print(f'{i}: {globals()[i].__doc__}')
        try:
            globals()[i]()
            print('Успех')
        except Exception as e:
            print('Неудача ', e)
