from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from postings.models import BlogPost
User = get_user_model()
class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_object = User(username="testuser", email="testuser@gmail.com")
        user_object.set_password("testuser") #sets password for our user
        user_object.save()
        blog_post = BlogPost.objects.create(user=user_object, 
        title="some blog post", content="some content")


    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count,1)