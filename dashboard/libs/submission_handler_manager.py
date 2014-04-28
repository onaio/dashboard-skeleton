class NoAppropriateHandlerException(Exception):
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