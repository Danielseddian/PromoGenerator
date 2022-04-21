import tempfile
from PromoGenerator.settings import *
from django.test import TestCase
from generator.models import User, Group, Promo, ExtAccess

MEDIA_ROOT = join(tempfile.gettempdir(), "test_media")


class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "Someone"
        cls.password = "Somepass113355"
        cls.group_name = "Somegroup"
        cls.file_name = "Somefile.txt"
        cls.user = User.objects.create_user(username=cls.username, password=cls.password)

    def setUp(self):
        pass

    def tearDown(self) -> None:
        pass

    def test_create(self):
        with open(BASE_DIR + "\\" + self.file_name, "w") as file:
            file.write("some thing")
        group = Group.objects.create(group=self.group_name, author=self.user, download=self.file_name)
