import unittest

from dashboard.libs import (
    SubmissionHandlerManager, SubmissionHandler, GenericSubmissionHandler,)


class TestSubmissionHandlerManager(unittest.TestCase):
    class Handler1(object):
        @staticmethod
        def can_handle(*args):
            return True

    def setUp(self):
        super(TestSubmissionHandlerManager, self).setUp()
        self.handler_manager = SubmissionHandlerManager()

    def test_add_handler_if_not_exist(self):
        self.assertNotIn(self.Handler1, self.handler_manager)
        self.handler_manager.add_handler(self.Handler1)
        self.assertIn(self.Handler1, self.handler_manager)

    def test_keep_handler_if_exists(self):
        self.handler_manager.add_handler(self.Handler1)
        self.handler_manager.add_handler(self.Handler1)
        self.assertIn(self.Handler1, self.handler_manager)
        self.assertEqual(len(self.handler_manager), 1)

    def test_find_handler_returns_first_handler_found(self):
        class Handler2(object):
            @staticmethod
            def can_handle(*args):
                return True

        handler_manager = SubmissionHandlerManager()
        # add handler2 first to make sure our order is maintained
        handler_manager.add_handler(Handler2)
        handler_manager.add_handler(self.Handler1)
        handler = handler_manager.find_handler({})
        self.assertEqual(handler, Handler2)

    def test_clear(self):
        handler_manager = SubmissionHandlerManager()
        handler_manager.add_handler(1)
        self.assertEqual(len(handler_manager), 1)
        handler_manager.clear()
        self.assertEqual(len(handler_manager), 0)


class TestSubmissionHandler(unittest.TestCase):
    def test_raise_not_implemented_on_can_handle(self):
        self.assertRaises(NotImplementedError, SubmissionHandler.can_handle)

    def test_raise_not_implemented_on_call(self):
        self.assertRaises(NotImplementedError, SubmissionHandler().__call__)


class TestGenericSubmissionHandler(unittest.TestCase):
    def test_always_returns_true_to_can_handle(self):
        self.assertTrue(GenericSubmissionHandler.can_handle("anything"))

    def test_always_return_true_to_call(self):
        self.assertTrue(GenericSubmissionHandler().__call__({}))