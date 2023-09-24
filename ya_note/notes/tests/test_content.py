from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.forms import NoteForm
from notes.models import Note

from .fixtures import FORM_URLS, SLUG, URL_NOTES_LIST

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Тестовый автор')
        cls.author_two = User.objects.create(username='Тестовый автор Два')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG,
            author=cls.author,
        )
        cls.note_author_two = Note.objects.create(
            title='Заголовок автор Два',
            text='Текст автор Два',
            slug='slug-post-author-two',
            author=cls.author_two,
        )

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(self.author)

    def test_notes_count(self):
        """
        В список заметок одного пользователя
        не попадают заметки другого пользователя
        """
        count_initial = Note.objects.filter(author=self.author).count()
        response = self.auth_client.get(URL_NOTES_LIST)
        object_list = response.context['object_list']

        self.assertEqual(len(object_list), count_initial)

    def test_pages_contains_form(self):
        """
        На страницы создания и редактирования заметки передаются формы
        """
        for name in FORM_URLS:
            with self.subTest(name=name):
                response = self.auth_client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)

    def test_note_correct_display_on_list(self):
        """
        Отдельная заметка передаётся на страницу со списком заметок
        в списке object_list в словаре context
        """
        response = self.auth_client.get(URL_NOTES_LIST)
        object_list = response.context['object_list']
        note = object_list.get(pk=self.note.pk)

        self.assertIn(self.note, object_list)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
