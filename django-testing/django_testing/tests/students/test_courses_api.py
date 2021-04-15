import pytest
from django.urls import reverse
from random import randint, choice
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_course_retrieve(api_client, student_factory, course_factory):
    course = course_factory(_quantity=1, students=student_factory())[0]
    url = reverse('courses-detail', args=[course.id])
    resp = api_client.get(url)
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == course.id


@pytest.mark.django_db
def test_course_list(api_client, student_factory, course_factory):
    courses = course_factory(
        _quantity=randint(1, 20), students=student_factory()
        )
    url = reverse('courses-list')
    resp = api_client.get(url)
    resp_json = resp.json()
    resp_ids = {course['id'] for course in resp_json}
    assert resp.status_code == HTTP_200_OK
    assert resp_ids == {course.id for course in courses}


@pytest.mark.django_db
def test_course_filter_by_id(api_client, student_factory, course_factory):
    courses = course_factory(
        _quantity=randint(1, 20), students=student_factory()
        )
    course_id = choice(courses).id
    url = reverse('courses-list')
    resp = api_client.get(url, {'id': course_id})
    resp_json = resp.json()[0]
    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == course_id


@pytest.mark.django_db
def test_course_filter_by_name(api_client, student_factory, course_factory):
    courses = course_factory(
        _quantity=randint(1, 20), students=student_factory()
        )
    name = choice(courses).name
    url = reverse('courses-list')
    resp = api_client.get(url, {'name': name})
    resp_json = resp.json()
    resp_names = {course['name'] for course in resp_json}
    course_names = set(filter(lambda x: x == name, resp_names))
    assert resp.status_code == HTTP_200_OK
    assert resp_names == course_names


@pytest.mark.django_db
def test_course_create(api_client, student_factory):
    students = student_factory()
    url = reverse('courses-list')
    payload = {
        'name': 'test',
        'students': [student.id for student in students]
    }
    resp = api_client.post(url, payload, format='json')
    resp_json = resp.json()
    assert resp.status_code == HTTP_201_CREATED
    assert resp_json['name'] == payload['name']
    assert resp_json['students'] == payload['students']


@pytest.mark.django_db
def test_course_update(api_client, student_factory, course_factory):
    courses = course_factory(
        _quantity=randint(1, 20), students=student_factory()
        )
    course = choice(courses)
    url = reverse('courses-detail', args=[course.id])
    payload = {
        'name': f'{course.name}_test'
    }
    resp = api_client.patch(url, payload, format='json')
    resp_json = resp.json()
    assert resp.status_code == HTTP_200_OK
    assert resp_json['id'] == course.id
    assert resp_json['name'] == payload['name']


@pytest.mark.django_db
def test_course_delete(api_client, student_factory, course_factory):
    courses = course_factory(
        _quantity=randint(1, 20), students=student_factory()
        )
    course_id = choice(courses).id
    url = reverse('courses-detail', args=[course_id])
    resp = api_client.delete(url)
    courses_ids = {
        course[id] for course in api_client.get(reverse('courses_list')).json()
        }
    assert resp.status_code == HTTP_204_OK
    assert course_id is not in courses_ids
