from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError

from news.forms import WARNING
from news.models import Comment

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client,
                                            form_data,
                                            news_detail_url,
                                            news_detail_redirect_url):
    """
    Анонимный пользователь не может отправить комментарий
    """
    count_initial_comments = Comment.objects.count()
    client.post(news_detail_url, data=form_data)
    count_after_comments = Comment.objects.count()

    assert count_initial_comments == count_after_comments


def test_user_can_create_comment(
        author, author_client, news, form_data, comment,
        news_detail_url, news_comment_redirect):
    """
    Авторизованный пользователь может отправить комментарий
    """
    count_initial_comments = Comment.objects.count()
    author_client.post(news_detail_url, data=form_data)

    comments_after = Comment.objects.all()
    count_after_comments = comments_after.count() - count_initial_comments
    comment = comments_after.last()

    assert 1 == count_after_comments
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(admin_client,
                                 bad_words_data,
                                 news_detail_url):
    """
    Если комментарий содержит запрещённые слова,
    он не будет опубликован, а форма вернёт ошибку
    """
    count_initial_comments = Comment.objects.count()
    response = admin_client.post(news_detail_url, data=bad_words_data)
    assertFormError(response, form='form', field='text', errors=WARNING)
    count_after_comments = Comment.objects.count()

    assert count_initial_comments == count_after_comments


def test_author_can_edit_comment(
        author_client,
        comment,
        form_data,
        news_edit_url,
        news_comment_redirect):
    """
    Авторизованный пользователь может редактировать свои комментарии
    """
    initial_comment_author = comment.author
    initial_comment_news = comment.news
    author_client.post(news_edit_url, data=form_data)
    comment.refresh_from_db()

    assert comment.text == form_data['text']
    assert comment.news == initial_comment_news
    assert comment.author == initial_comment_author


def test_author_can_delete_comment(
        author_client,
        comment,
        news_delete_url,
        news_comment_redirect):
    """
    Авторизованный пользователь может удалять свои комментарии
    """
    author_client.post(news_delete_url)

    assert not Comment.objects.filter(pk=comment.pk).exists()


def test_other_user_cant_edit_comment(
        admin_client, comment, form_data, news_edit_url):
    """
    Авторизованный пользователь не может редактировать чужие комментарии
    """
    initial_comment_author = comment.author
    initial_comment_news = comment.news
    old_comment_text = comment.text
    response = admin_client.post(news_edit_url, data=form_data)
    comment.refresh_from_db()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.text == old_comment_text
    assert comment.news == initial_comment_news
    assert comment.author == initial_comment_author


def test_other_user_cant_delete_comment(
        admin_client, comment, news_delete_url):
    """
    Авторизованный пользователь не может  удалять чужие комментарии
    """
    count_initial_comments = Comment.objects.count()
    initial_comment_author = comment.author
    initial_comment_news = comment.news
    initial_comment_text = comment.text
    response = admin_client.post(news_delete_url)
    count_after_comments = Comment.objects.count()
    comment.refresh_from_db()

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment.news == initial_comment_news
    assert comment.author == initial_comment_author
    assert comment.text == initial_comment_text
    assert count_initial_comments == count_after_comments
