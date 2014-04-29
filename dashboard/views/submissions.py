import json
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.httpexceptions import HTTPBadRequest

from base import BaseView
from dashboard.libs.submission_handler import (
    NoAppropriateHandlerException,
    submission_handler_manager,
    SubmissionHandlerError)


@view_defaults(route_name='submissions')
class Submissions(BaseView):
    @view_config(
        name='',
        request_method='POST',
        permission=NO_PERMISSION_REQUIRED)
    def json_post(self):
        payload = self.request.body
        if not payload:
            return HTTPBadRequest(comment='Missing JSON Payload')

        try:
            json_payload = json.loads(payload)
        except ValueError:
            return HTTPBadRequest(comment='Invalid JSON Payload')

        try:
            handler = submission_handler_manager.find_handler(json_payload)
        except NoAppropriateHandlerException:
            return HTTPBadRequest(comment='Handler could not be determined')
        else:
            try:
                handler().__call__(json_payload)
            except SubmissionHandlerError:
                return Response(
                    'Accepted pending manual matching process', status=202)
            else:
                return Response('Saved', status=201)