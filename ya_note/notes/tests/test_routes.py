from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

from .fixtures import (AUTHOR_URLS, ONLY_AUTH_URLS, PUBLIC_URLS,
                       REDIRECTS_ANONYM, SLUG)

User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Тестовый автор')
        cls.reader = User.objects.create(username='Тестовый читатель')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG,
            author=cls.author)

    def setUp(self):
        self.client_author = Client()
        self.client_author.force_login(self.author)
        self.client_reader = Client()
        self.client_reader.force_login(self.reader)

    def test_overall_availability(self):
        """
        Главная страница доступна анонимному пользователю.

        Аутентифицированному пользователю доступна страница со списком заметок
        notes/, страница успешного добавления заметки done/,
        страница добавления новой заметки add/.


        Страницы отдельной заметки, удаления и редактирования заметки доступны
        только автору заметки. Если на эти страницы попытается зайти
        другой пользователь — вернётся ошибка 404.

        При попытке перейти на страницу списка заметок, страницу успешного
        добавления записи, страницу добавления заметки, отдельной заметки,
        редактирования или удаления заметки анонимный пользователь
        перенаправляется на страницу логина.

        Страницы регистрации пользователей, входа в учётную запись и
        выхода из неё доступны всем пользователям.
        """
        availability_data = (

            (self.client,
             ONLY_AUTH_URLS + AUTHOR_URLS,
             HTTPStatus.FOUND),

            (self.client_reader,
             AUTHOR_URLS,
             HTTPStatus.NOT_FOUND),

            (self.client, PUBLIC_URLS, HTTPStatus.OK),
            (self.client_reader, ONLY_AUTH_URLS + PUBLIC_URLS, HTTPStatus.OK),

            (self.client_author,
             ONLY_AUTH_URLS + AUTHOR_URLS + PUBLIC_URLS,
             HTTPStatus.OK),
        )

        for case in availability_data:
            client, urls, status = case
            for url in urls:
                with self.subTest(url=url, client=client, status=status):
                    response = client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_overall_redirect(self):
        """
        Проверка редиректов анонимного пользователя
        """
        for url, redirect_url in REDIRECTS_ANONYM:
            with self.subTest(url=url, redirect_url=redirect_url):
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
