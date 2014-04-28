class NoAppropriateHandlerException(Exception):
    pass


class SubmissionHandlerError(Exception):
    pass


class SubmissionHandlerManager(list):
    def add_handler(self, handler):
        try:
            self.index(handler)
        except ValueError:
            self.append(handler)

    def find_handler(self, json_payload):
        for handler in iter(self):
            if handler.can_handle(json_payload):
                return handler
        else:
            raise NoAppropriateHandlerException

    def clear(self):
        self[0:] = []


class SubmissionHandler(object):
    """
    Abstract submission handler
    """
    @staticmethod
    def can_handle(*args, **kwargs):
        raise NotImplementedError("You must implement can_handle")

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("You must implement can_handle")


class GenericSubmissionHandler(object):
    """
    A handler that always says 'yes'
    """
    @staticmethod
    def can_handle(json_payload):
        return True

    def __call__(self, json_payload):
        return True

submission_handler_manager = SubmissionHandlerManager()