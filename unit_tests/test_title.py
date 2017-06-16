from title_api.main import app
from title_api.extensions import db
from title_api.models import Title
import json
from unittest import TestCase, mock

db_response_list = list()
title = Title(foo='testing', bar='still_testing')
db_response_list.append(title)

standard_dict = {"foo": "badger",
                 "bar": "mushroom"}


class TestTitle(TestCase):

    def setUp(self):
        self.app = app.test_client()

    @mock.patch.object(db.Model, 'query')
    def test_001_happy_path_get(self, mock_db_query):
        mock_db_query.order_by.return_value.all.return_value = db_response_list
        resp = self.app.get('/v1/titles', headers={'accept': 'application/json'})
        self.assertEqual(resp.status_code, 200)
        assert 'created_at' in resp.get_data().decode()
        assert '"foo":"testing"' in resp.get_data().decode()
        assert '"bar":"still_testing"' in resp.get_data().decode()

    @mock.patch.object(db.session, 'commit')
    @mock.patch.object(db.session, 'add')
    def test_002_happy_path_post(self, mock_db_add, mock_db_commit):
        resp = self.app.post('/v1/titles', data=json.dumps(standard_dict),
                             headers={'content-type': 'application/json', 'accept': 'application/json'})
        self.assertEqual(resp.status_code, 201)
        # Check we call the correct two database methods
        self.assertTrue(mock_db_add.called)
        self.assertTrue(mock_db_commit.called)
