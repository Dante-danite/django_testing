import pytest
from django.conf import settings

from news.forms import CommentForm

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('many_news')
def test_news_count(client, news_home_url):
    """Количество новостей на главной странице — не более 10"""
    response = client.get(news_home_url)
    objects = response.context['object_list']

    assert len(objects) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('many_news')
def test_news_order(client, news_home_url):
    """
    Новости отсортированы от самой свежей к самой старой.
    Свежие новости в начале списка
    """
    response = client.get(news_home_url)
    objects = response.context['object_list']
    all_dates = [news.date for news in objects]

    assert all_dates == sorted(all_dates, reverse=True)


@pytest.mark.parametrize(
    'url, user, has_access', ((pytest.lazy_fixture('news_detail_url'),
                               pytest.lazy_fixture('author_client'),
                               True),
                              (pytest.lazy_fixture('news_detail_url'),
                               pytest.lazy_fixture('client'),
                               False))
)
def test_comment_form_availability_for_different_users(user, has_access, url):
    """
    Анонимному пользователю недоступна форма для отправки комментария
    на странице отдельной новости, а авторизованному доступна
    """
    context = user.get(url).context

    assert has_access == ('form' in context)


def test_comment_form_author_user(author_client,
                                  news_detail_url):
    """
    Авторизованному пользователю представлена форма
    для отправки комментария на странице отдельной
    новости
    """
    context = author_client.get(news_detail_url).context

    assert isinstance(context['form'], CommentForm)


@pytest.mark.usefixtures('many_comments')
def test_comments_order(client, news_detail_url):
    """
    Комментарии на странице отдельной новости
    отсортированы в хронологическом порядке:
    старые в начале списка, новые — в конце
    """
    response = client.get(news_detail_url)
    context_news = response.context['news']
    all_comments = context_news.comment_set.all()

    assert list(all_comments) == list(all_comments.order_by('created'))
