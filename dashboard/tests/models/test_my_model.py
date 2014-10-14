from dashboard.tests.test_base import TestBase
from dashboard.models.my_model import MyModel


class TestMyModel(TestBase):

    def test_get_or_create(self):
        model_1 = MyModel(name="name_1", value="value_1")
        model_1.save()
        self.assertIsNotNone(model_1.id)
        # Test retrieval

        kwargs = {'name': "name_1", 'value': 'value_1'}
        name_criteria = MyModel.name == kwargs["name"]
        instance = MyModel.get_or_create(name_criteria, **kwargs)
        self.assertEqual(model_1.id, instance.id)

        # Test addition
        kwargs = {'name': "name_2", 'value': 'value_2'}
        name_criteria = MyModel.name == kwargs["name"]
        instance = MyModel.get_or_create(name_criteria, **kwargs)
        self.assertNotEqual(model_1.id, instance.id)
