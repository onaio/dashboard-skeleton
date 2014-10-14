from pyramid.httpexceptions import HTTPBadRequest

from dashboard.libs import (
    GenericSubmissionHandler, SubmissionHandlerError)
from dashboard.libs.submission_handler import submission_handler_manager
from dashboard.tests.test_base import TestBase
from dashboard.views.submissions import Submissions


class TestSubmissions(TestBase):
    def setUp(self):
        super(TestSubmissions, self).setUp()
        self.submission_views = Submissions(self.request)
        submission_handler_manager.clear()

    def test_json_post_returns_400_on_empty_payload(self):
        self.request.method = 'POST'
        response = self.submission_views.json_post()
        self.assertIsInstance(response, HTTPBadRequest)

    def test_json_post_returns_400_on_invalid_json(self):
        self.request.method = 'POST'
        self.request.body = "some bad json"
        response = self.submission_views.json_post()
        self.assertIsInstance(response, HTTPBadRequest)

    def test_json_post_returns_bad_request_on_missing_handler(self):
        self.request.method = 'POST'
        self.request.body = '{"_xform_id_string": "abcd"}'
        response = self.submission_views.json_post()
        self.assertIsInstance(response, HTTPBadRequest)

    def test_json_post_returns_202_on_handler_error(self):
        class ErrorSubmissionHandler(GenericSubmissionHandler):
            def __call__(self, request, json_payload):
                raise SubmissionHandlerError()

        submission_handler_manager.add_handler(ErrorSubmissionHandler)
        self.request.method = 'POST'
        self.request.body = '{"_xform_id_string": "abcd"}'
        response = self.submission_views.json_post()
        self.assertEqual(response.status_code, 202)

    def test_json_post_returns_201_on_successful_handling(self):
        submission_handler_manager.add_handler(GenericSubmissionHandler)
        self.request.method = 'POST'
        self.request.body = '{"_xform_id_string": "abcd"}'
        response = self.submission_views.json_post()
        self.assertEqual(response.status_code, 201)
