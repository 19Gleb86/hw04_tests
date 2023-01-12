from http import HTTPStatus

from django.test import Client, TestCase
from posts.models import Group, Post, User


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='NoName')
        cls.some_user = User.objects.create(username='some_user')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

        cls.INDEX = '/'
        cls.GROUP_LIST = f'/group/{cls.group.slug}/'
        cls.PROFILE_temp = f'/profile/{cls.user}/'
        cls.PROFILE = f'/profile/{cls.user.username}/'
        cls.POST_DETAIL = f'/posts/{cls.post.id}/'
        cls.POST_EDIT = f'/posts/{cls.post.id}/edit/'
        cls.POST_CREATE = '/create/'
        cls.FAKE_PAGE = '/unexisting_page/'

        cls.templates_url_names_public = {
            cls.INDEX: 'posts/index.html',
            cls.GROUP_LIST: 'posts/group_list.html',
            cls.PROFILE: 'posts/profile.html',
            cls.POST_DETAIL: 'posts/post_detail.html',
        }
        cls.templates_url_names_private = {
            cls.POST_EDIT: 'posts/create_post.html',
            cls.POST_CREATE: 'posts/create_post.html',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.another_authorized_client = Client()
        self.another_authorized_client.force_login(self.some_user)

    def test_public_urls_with_guest_client(self):
        """Публичные страницы доступны гостевым учеткам"""
        for adress in self.templates_url_names_public:
            with self.subTest(adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)
    
    def test_private_url_with_guest_client(self):
        """Страницы POST_EDIT и POST_CREATE перенаправляют гостевую учетку."""
        for adress in self.templates_url_names_private:
            with self.subTest(adress):
                response = self.guest_client.get(adress, follow=True)
        self.assertRedirects(response, f'/auth/login/?next={adress}')

    def test_posts_post_id_edit_url_exists_at_author(self):
        """Страница POST_EDIT доступна автору."""
        self.user = User.objects.get(username=self.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.get(self.POST_EDIT)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_with_authorized_client(self):
        """Страница POST_CREATE доступна авторизованному пользователю."""
        self.user = User.objects.get(username=self.user)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.get(self.POST_CREATE)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_public_urls_uses_correct_template(self):
        """Публичные URL-адреса используют соответствующие шаблоны."""
        for url, template in self.templates_url_names_public.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)
    
    def test_private_urls_uses_correct_template(self):
        """Приватные URL-адреса используют соответствующие шаблоны."""
        for url, template in self.templates_url_names_private.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_posts_post_id_edit_url_with_non_author_client(self):
        """Страница POST_EDIT доступна только автору."""
        self.authorized_client.force_login(self.some_user)
        response = self.another_authorized_client.get(self.POST_EDIT, follow=True)
        self.assertRedirects(response, self.POST_DETAIL)

    def test_unexisting_page_at_desired_location(self):
        """Страница FAKE_PAGE должна выдать ошибку."""
        response = self.guest_client.get(self.FAKE_PAGE)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
