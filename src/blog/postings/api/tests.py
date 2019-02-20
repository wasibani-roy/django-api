from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from postings.models import BlogPost


User = get_user_model()
paylaod_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


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

    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        #testing retriving posts
        data = {}
        url = api_reverse("post-create")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item_no_user(self):
        data = {
            "title": "some test post",
            "content": "this is a test post"
        }
        url = api_reverse("post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {
            "title": "some test post",
            "content": "this is a test post"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {
            "title": "some test post",
            "content": "this is a test post"
        }
        user_obj = User.objects.first()
        payload = paylaod_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response) #how you set a header for a token
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_post_item(self):
        data = {
            "title": "some test post",
            "content": "this is a test post"
        }
        user_obj = User.objects.first()
        payload = paylaod_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response)
        url = api_reverse("post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(username='tom')
        blog_post = BlogPost.objects.create(user=owner, 
        title="some blog post", content="some content")
        user_obj = User.objects.first()
        #checking to see that users usernames are different
        self.assertNotEqual(user_obj.username, owner.username)

        #creating token for user defined in our setup
        payload = paylaod_handler(user_obj)
        token_response = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_response)
        url = blog_post.get_api_url()
        data = {
            "title": "some test post",
            "content": "this is a test post"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_login_and_update(self):
        data = {
            'username':'testuser',
            'password':'testuser'
        }
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get('token')
        if token is not None:
            blog_post = BlogPost.objects.first()
            url = blog_post.get_api_url()
            data = {
                "title": "some test post",
                "content": "this is a test post"
            }
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

