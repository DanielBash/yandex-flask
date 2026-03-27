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


def test_delete_job():
    """Тест удаления работы"""
    response = requests.delete(
        "http://127.0.0.1:5000/api/jobs/delete/1").json()


def test_edit_job():
    """Редактирование работы"""
    params = {
        "job": "Updated login system",
        "team_leader": 1,
        "collaborators": "2, 3",
        "is_finished": "true",
        "work_size": 15,
        "category": 2
    }
    response = requests.put(
        "http://127.0.0.1:5000/api/jobs/1",
        params=params
    )


def test_edit_job_not_found():
    """Редактирование несуществующей работы"""
    params = {"job": "Nonexistent update"}
    response = requests.put(
        "http://127.0.0.1:5000/api/jobs/999",
        params=params
    )


def test_edit_job_wrong_work_size():
    """Редактирование с неверной сложностью"""
    params = {
        "job": "Bad work_size",
        "work_size": "abc"
    }
    response = requests.put(
        "http://127.0.0.1:5000/api/jobs/1",
        params=params
    )


def test_edit_job_partial():
    """Частичное редактирование (только job)"""
    params = {"job": "Partial update"}
    response = requests.put(
        "http://127.0.0.1:5000/api/jobs/1",
        params=params
    )


def test_get_single_user_v2():
    """Получение одного пользователя v2"""
    requests.get('http://localhost:5000/api/v2/users/1').json()


def test_get_multiple_users_v2():
    """Получение всех пользователей v2"""
    print(requests.get('http://localhost:5000/api/v2/users').json())


def test_get_single_user_wrong_id_v2():
    """Получение пользователя с неверным id v2"""
    requests.get('http://localhost:5000/api/v2/users/-1').json()


def test_get_single_user_string_id_v2():
    """Получение пользователя с неверным id-строкой v2"""
    requests.get('http://localhost:5000/api/v2/users/test_string').json()


def test_add_user_v2():
    """Создание пользователя v2"""
    params = {
        "surname": "Иванов",
        "name": "Иван",
        "age": 30,
        "position": "Developer",
        "speciality": "Python",
        "address": "Москва",
        "email": "ivan@example.com",
        "hashed_password": "hashedpass123"
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/v2/users",
        params=params
    ).json()


def test_add_user_missing_email_v2():
    """Создание пользователя без email v2"""
    params = {
        "surname": "Иванов",
        "name": "Иван",
        "hashed_password": "hashedpass123"
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/v2/users",
        params=params
    ).json()


def test_add_user_missing_password_v2():
    """Создание пользователя без пароля v2"""
    params = {
        "surname": "Иванов",
        "name": "Иван",
        "email": "ivan@example.com"
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/v2/users",
        params=params
    ).json()


def test_delete_user_v2():
    """Тест удаления пользователя v2"""
    response = requests.delete(
        "http://127.0.0.1:5000/api/v2/users/1").json()


def test_delete_user_not_found_v2():
    """Удаление несуществующего пользователя v2"""
    response = requests.delete(
        "http://127.0.0.1:5000/api/v2/users/999").json()


def test_edit_user_v2():
    """Полное редактирование пользователя v2"""
    params = {
        "surname": "Петров",
        "name": "Петр",
        "age": 35,
        "position": "Senior Developer",
        "speciality": "Backend",
        "address": "СПб",
        "email": "petr@example.com",
        "hashed_password": "newhashedpass456"
    }
    response = requests.put(
        "http://127.0.0.1:5000/api/v2/users/1",
        params=params
    ).json()


def test_edit_user_not_found_v2():
    """Редактирование несуществующего пользователя v2"""
    params = {"surname": "Nonexistent"}
    response = requests.put(
        "http://127.0.0.1:5000/api/v2/users/999",
        params=params
    ).json()


def test_edit_user_partial_v2():
    """Частичное редактирование"""
    params = {"surname": "Сидоров"}
    response = requests.put(
        "http://127.0.0.1:5000/api/v2/users/1",
        params=params
    ).json()


def test_edit_user_wrong_age_v2():
    """Редактирование с неверным возрастом v2"""
    params = {
        "surname": "Bad age",
        "age": "abc"
    }
    response = requests.put(
        "http://127.0.0.1:5000/api/v2/users/1",
        params=params
    ).json()


def test_get_single_job_v2():
    """Получение одной работы v2"""
    response = requests.get('http://localhost:5000/api/v2/jobs/1').json()


def test_get_multiple_jobs_v2():
    """Получение нескольких работ v2"""
    response = requests.get('http://localhost:5000/api/v2/jobs').json()
    assert 'jobs' in response
    print(response)


def test_add_job_v2():
    """Создание работы v2"""
    params = {
        "is_finished": False,
        "job": "Develop login system",
        "collaborators": "1, 2",
        "team_leader": 1,
        "work_size": 10,
        "category": 1
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/v2/jobs",
        params=params
    ).json()


def test_add_job_wrong_team_leader_v2():
    """Неверное создание работы c лидером-строкой v2"""
    params = {
        "is_finished": False,
        "job": "Develop login system",
        "collaborators": "1, 2",
        "team_leader": "1",
        "work_size": 10,
        "category": 1
    }
    response = requests.post(
        "http://127.0.0.1:5000/api/v2/jobs",
        params=params
    ).json()


def test_delete_job_v2():
    """Тест удаления работы v2"""
    response = requests.delete(
        "http://127.0.0.1:5000/api/v2/jobs/1").json()


def test_edit_job_v2():
    """Полное редактирование работы v2"""
    params = {
        "job": "Updated login system",
        "team_leader": 1,
        "collaborators": "2, 3",
        "is_finished": "true",
        "work_size": 15,
        "category": 2
    }
    response = requests.put(
        "http://127.0.0.1:5000/api/v2/jobs/1",
        params=params
    ).json()


def test_edit_job_not_found_v2():
    """Редактирование несуществующей работы v2"""
    params = {"job": "Nonexistent update"}
    response = requests.put(
        "http://127.0.0.1:5000/api/v2/jobs/999",
        params=params
    ).json()


def test_edit_job_wrong_work_size_v2():
    """Редактирование с неверной сложностью v2"""
    params = {
        "job": "Bad work_size",
        "work_size": "abc"
    }
    response = requests.put(
        "http://127.0.0.1:5000/api/v2/jobs/1",
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
