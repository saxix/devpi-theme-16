# -*- coding: utf-8 -*-
# flake8: noqa: E501
import json
import re

import pytest


def compareable_text(text):
    return re.sub('\s+', ' ', text.strip())


def clean(text):
    return text.replace('\n', '').strip()


@pytest.yield_fixture
def pyramidconfig():
    from pyramid.testing import setUp, tearDown
    from devpi_theme_16.main import includeme
    config = setUp()
    includeme(config)
    yield config
    tearDown()


@pytest.yield_fixture
def dummyrequest(pyramidconfig):
    from pyramid.testing import DummyRequest
    request = DummyRequest()
    pyramidconfig.begin(request=request)
    yield request


def test_login_success(testapp):
    r = testapp.get('/+login2', headers=dict(accept="text/html"))
    assert r.status_code == 200

    r = testapp.post('/+login2',
                     params={'username': 'root', 'password': ''})
    assert r.status_code == 302


def test_login_fail(testapp):
    r = testapp.get('/+login2', headers=dict(accept="text/html"))
    assert r.status_code == 200

    r = testapp.post('/+login2',
                     params={'username': 'inv@lid', 'password': ''},
                     headers=dict(accept="text/html"))
    assert r.status_code == 200
    # assert r.body.index("Invalid credentials")


def test_logout(testapp):
    r = testapp.get('/+logout',
                    follow=False,
                    headers=dict(accept="text/html"))
    assert r.status_code == 302


def test_info_view(testapp):
    r = testapp.get('/+info', headers=dict(accept="text/html"))
    assert r.status_code == 200


def test_help_view(testapp):
    r = testapp.get('/+searchhelp', headers=dict(accept="text/html"))
    assert r.status_code == 200


def test_user_view(testapp):
    r = testapp.get('/root', headers=dict(accept="text/html"))
    assert r.status_code == 200


def test_root_view(testapp):
    r = testapp.get('/', headers=dict(accept="text/html"))
    assert r.status_code == 200
    links = r.html.select('#content a')
    assert [(compareable_text(l.text), l.attrs['href']) for l in links] == [
        (u'root', u'/root'),
        (u'root/pypi PyPI', u'http://localhost/root/pypi')]


def test_index_view_project_info(mapp, testapp):
    api = mapp.create_and_use(indexconfig=dict(bases=["root/pypi"]))
    mapp.set_versiondata({"name": "pkg1", "version": "2.6"})
    r = testapp.get(api.index, headers=dict(accept="text/html"))
    assert r.status_code == 200
    links = r.html.select('#content a')
    assert [(l.text, l.attrs['href']) for l in links] == [
        ("show full list", "http://localhost/%s/+simple/" % api.stagename),
        ("pkg1-2.6", "http://localhost/%s/pkg1/2.6" % api.stagename),
        ("root/pypi", "http://localhost/root/pypi"),
        ("simple", "http://localhost/root/pypi/+simple/")]


def test_index_view_project(mapp, testapp):
    api = mapp.create_and_use()
    mapp.upload_file_pypi(
        "pkg1-2.6.tar.gz", b"contentveryold", "pkg1", "2.6").file_url

    r = testapp.get("{}/pkg1".format(api.index), headers=dict(accept="text/html"))
    assert r.status_code == 200
    links = r.html.select('#content a')
    assert [(l.text, l.attrs['href']) for l in links] == [
        (u'user1/dev', u'http://localhost/user1/dev'),
        (u'2.6', u'http://localhost/user1/dev/pkg1/2.6')]


def test_index_view_project_version(mapp, testapp):
    api = mapp.create_and_use()
    mapp.upload_file_pypi(
        "pkg1-2.6.tar.gz", b"contentveryold", "pkg1", "2.6").file_url

    r = testapp.get("{}/pkg1/2.6".format(api.index), headers=dict(accept="text/html"))
    assert r.status_code == 200
    links = r.html.select('#content a')
    assert [(clean(l.text), l.attrs['href']) for l in links] == [
        (u'Simple index', u'http://localhost/user1/dev/+simple/pkg1'),
        (u'pkg1-2.6.tar.gz',
         u'http://localhost/user1/dev/+f/229/fe31ddfe94170/pkg1-2.6.tar.gz#sha256=229fe31ddfe9417012548d945e637febcf94efb3fe29935a248d7ceccb4a61f3'),
        (u'user1/dev', u'http://localhost/user1/dev'),
        (u'user1', u'/user1')]


@pytest.mark.with_notifier
def test_index_view_project_toxresults(mapp, testapp):
    from test_devpi_server.example import tox_result_data
    api = mapp.create_and_use()
    mapp.set_versiondata(
        {"name": "pkg1", "version": "2.6", "description": "foo"})
    mapp.upload_file_pypi(
        "pkg1-2.6.tgz", b"123", "pkg1", "2.6", code=200, waithooks=True)
    path, = mapp.get_release_paths("pkg1")
    r = testapp.post(path, json.dumps(tox_result_data))

    r = testapp.get("{}/pkg1/2.6/+toxresults/pkg1-2.6.tgz".format(api.index), headers=dict(accept="text/html"))
    assert r.status_code == 200
    links = r.html.select('#content a')
    assert [(clean(l.text), l.attrs['href']) for l in links] == [
        (u'No setup performed',
         u'http://localhost/user1/dev/pkg1/2.6/+toxresults/pkg1-2.6.tgz/pkg1-2.6.tgz.toxresult0#foo-linux2-py27-setup'),
        (u'Tests',
         u'http://localhost/user1/dev/pkg1/2.6/+toxresults/pkg1-2.6.tgz/pkg1-2.6.tgz.toxresult0#foo-linux2-py27-test')]


def test_index_remove_project_query(mapp, testapp):
    api = mapp.create_and_use()
    mapp.upload_file_pypi(
        "pkg1-2.6.tar.gz", b"contentveryold", "pkg1", "2.6").file_url

    r = testapp.get("{}/pkg1/2.6/+remove".format(api.index),
                    headers=dict(accept="text/html"))
    assert r.status_code == 200
    # assert r.body.index("Confirm permanent removal of") > 0


def test_index_remove_cancel(mapp, testapp):
    api = mapp.create_and_use()
    mapp.upload_file_pypi(
        "pkg1-2.6.tar.gz", b"contentveryold", "pkg1", "2.6").file_url

    r = testapp.post("{}/pkg1/2.6/+remove".format(api.index),
                     params={"cancel": 1})
    assert r.status_code == 302

    r = testapp.get("{}/pkg1/2.6/+remove".format(api.index),
                    headers=dict(accept="text/html"))
    assert r.status_code == 200


def test_index_remove_confirm(mapp, testapp):
    api = mapp.create_and_use()
    mapp.upload_file_pypi(
        "pkg1-2.6.tar.gz", b"contentveryold", "pkg1", "2.6").file_url

    r = testapp.post("{}/pkg1/2.6/+remove".format(api.index),
                     params={"remove": 1})
    assert r.status_code == 302

    r = testapp.get("{}/pkg1/2.6/+remove".format(api.index),
                    headers=dict(accept="text/html"))
    assert r.status_code == 404
