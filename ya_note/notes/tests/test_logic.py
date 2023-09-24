from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .fixtures import (SLUG, URL_NOTES_ADD, URL_NOTES_DELETE, URL_NOTES_EDIT,
                       URL_NOTES_SUCCESS)

User = get_user_model()


class TestNoteCreation(TestCase):
    NOTE_TEXT = 'Текст'
    NOTE_TITLE = 'Заголовок'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Тестовый автор')
        cls.another_author = User.objects.create(username='Другой автор')

        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
            'slug': 'slug1'
        }
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            slug=SLUG,
            author=cls.author,
        )
        cls.form_data_no_slug = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT,
        }

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(self.author)
        self.auth_another_author = Client()
        self.auth_another_author.force_login(self.another_author)

    def test_anonymous_user_cant_create_notes(self):
        """
        Анонимный пользователь не может создать заметку
        """
        initial_notes = Note.objects.count()
        self.client.post(URL_NOTES_ADD, data=self.form_data)
        after_notes = Note.objects.count()

        self.assertEqual(after_notes, initial_notes)

    def test_user_can_create_notes(self):
        """
        Залогиненный пользователь может создать заметку
        """
        objects = Note.objects.all()
        notes_before_creation = objects.count()
        response = self.auth_another_author.post(URL_NOTES_ADD,
                                                 data=self.form_data)
        created_notes = objects.count() - notes_before_creation

        self.assertTrue(created_notes, 1)
        self.assertRedirects(response, URL_NOTES_SUCCESS)
        self.assertEqual(objects.last().title, self.form_data['title'])
        self.assertEqual(objects.last().text, self.form_data['text'])
        self.assertEqual(objects.last().slug, self.form_data['slug'])
        self.assertEqual(objects.last().author, self.another_author)

    def test_not_unique_slug(self):
        """
        Невозможно создать две заметки с одинаковым slug
        """
        initial_notes = Note.objects.count()
        self.form_data['slug'] = self.note.slug
        response = self.auth_client.post(URL_NOTES_ADD, data=self.form_data)
        new_notes = Note.objects.count()

        self.assertEqual(new_notes, initial_notes)
        self.assertFormError(
            response, form='form',
            field='slug',
            errors=self.note.slug + WARNING
        )

    def test_empty_slug(self):
        """
        Если при создании заметки не заполнен slug,
        то он формируется автоматически,
        с помощью функции pytils.translit.slugify
        """
        objects = Note.objects.all()

        initial_notes = objects.count()
        response = self.auth_client.post(
            URL_NOTES_ADD,
            data=self.form_data_no_slug)
        created_notes = objects.count() - initial_notes
        expected_slug = slugify(self.form_data['title'])

        self.assertTrue(created_notes, 1)
        self.assertRedirects(response, URL_NOTES_SUCCESS)
        self.assertEqual(objects.last().title, self.form_data_no_slug['title'])
        self.assertEqual(objects.last().text, self.form_data_no_slug['text'])
        self.assertEqual(objects.last().slug, expected_slug)
        self.assertEqual(objects.last().author, self.author)


class TestEditAndDeleteNote(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NOTE_TITLE = 'Заголовок'
    EDITED_NOTE_TEXT = 'Измененный текст заметки'
    EDITED_NOTE_TITLE = 'Измененный заголовок'
    EDITED_NOTE_SLUG = 'edited_slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Тестовый автор')
        cls.reader = User.objects.create(username='Тестовый пользователь')
        cls.note = Note.objects.create(title=cls.NOTE_TITLE,
                                       text=cls.NOTE_TEXT,
                                       slug=SLUG,
                                       author=cls.author)

        cls.form_data = {
            'title': cls.EDITED_NOTE_TITLE,
            'text': cls.EDITED_NOTE_TEXT,
            'slug': cls.EDITED_NOTE_SLUG
        }

    def setUp(self):
        self.author_client = Client()
        self.author_client.force_login(self.author)
        self.reader_client = Client()
        self.reader_client.force_login(self.reader)

    def test_author_can_delete_note(self):
        """
        Пользователь может удалять свои заметки
        """
        response = self.author_client.delete(URL_NOTES_DELETE)

        self.assertRedirects(response, URL_NOTES_SUCCESS)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_reader_cant_delete_user_note(self):
        """
        Пользователь не может удалять чужие заметки
        """
        response = self.reader_client.delete(URL_NOTES_DELETE)
        note = Note.objects.get(id=self.note.id)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_edit_note(self):
        """
        Пользователь может изменять свои заметки
        """
        response = self.author_client.post(URL_NOTES_EDIT, data=self.form_data)
        note_from_db = Note.objects.get(pk=self.note.pk)

        self.assertRedirects(response, URL_NOTES_SUCCESS)
        self.assertEqual(note_from_db.title, self.form_data['title'])
        self.assertEqual(note_from_db.text, self.form_data['text'])
        self.assertEqual(note_from_db.slug, self.form_data['slug'])
        self.assertEqual(note_from_db.author, self.note.author)

    def test_reader_cant_edit_user_note(self):
        """
        Пользователь не может изменять чужие заметки
        """
        response = self.reader_client.post(URL_NOTES_EDIT, data=self.form_data)
        note_from_db = Note.objects.get(pk=self.note.pk)

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(note_from_db.text, self.note.text)
        self.assertEqual(note_from_db.title, self.note.title)
        self.assertEqual(note_from_db.slug, self.note.slug)
        self.assertEqual(note_from_db.author, self.note.author)
