import datetime
import pytest

from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.forms import BAD_WORDS
from news.models import Comment, News

CREATE_MANY_COMMENTS_COUNT = 5


@pytest.fixture
def author(django_user_model):
    """
    Фикстура создает и возвращает объект пользователя
    """
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    """
    Фикстура возвращает клиент с
    авторизованным пользователем
    """
    client.force_login(author)
    return client


@pytest.fixture
def bad_words_data():
    """
    Фикстура возвращает словарь с запрещенными словами
    """
    return {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}


@pytest.fixture
def news():
    """
    Фикстура создает и возвращает объект новости
    """
    news = News.objects.create(
        title='Заголовок',
        text='Текст',
    )
    return news


@pytest.fixture
def comment(news, author):
    """
    Фикстура создает и возвращает объект комментария
    """
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст'
    )
    return comment


@pytest.fixture
def many_news():
    """
    Фикстура создает объекты новостей в
    количестве из переменной settings.NEWS_COUNT_ON_HOME_PAGE
    """
    News.objects.bulk_create(
        News(title=f'Новость {index}',
             text='Текст',
             date=timezone.now() - datetime.timedelta(days=index)
             )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def many_comments(news, author):
    """
    Фикстура возвращает объекты новостей в
    количестве из переменной CREATE_MANY_COMMENTS_COUNT
    """
    now = timezone.now()
    for index in range(CREATE_MANY_COMMENTS_COUNT):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Текст {index}',
        )
        comment.created = now - datetime.timedelta(days=index)
        comment.save()


@pytest.fixture
def form_data():
    """
    Фикстура возвращает словарь с текстом
    """
    return {
        'text': 'Текст'
    }


@pytest.fixture
def users_login_url():
    """
     Фикстура возвращает ссылку из 'users:login'
     """
    return reverse('users:login')


@pytest.fixture
def users_logout_url(news):
    """
     Фикстура возвращает ссылку из 'users:logout'
     """
    return reverse('users:logout')


@pytest.fixture
def users_signup_url(news):
    """
     Фикстура возвращает ссылку из 'users:signup'
     """
    return reverse('users:signup')


@pytest.fixture
def news_home_url(news):
    """
     Фикстура возвращает ссылку из 'news:home'
     """
    return reverse('news:home')


@pytest.fixture
def news_detail_url(news):
    """
    Фикстура возвращает ссылку из 'news:detail'
    """
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def news_edit_url(comment):
    """
    Фикстура возвращает ссылку из 'news:edit'
    """
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def news_delete_url(comment):
    """
    Фикстура возвращает ссылку из 'news:delete'
    """
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def news_detail_redirect_url(users_login_url, comment):
    """
    Фикстура возвращает ссылку редиректа для логина и перехода к 'news:detail'
    """
    next_url = reverse('news:detail', args=(comment.pk,))
    return f"{users_login_url}?next={next_url}"


@pytest.fixture
def news_comment_redirect(news):
    """
    Фикстура возвращает ссылку редиректа 'news:detail' к '#comments'
    """
    return reverse('news:detail', args=(news.pk,)) + '#comments'


@pytest.fixture
def edit_redirect_url(users_login_url, news_edit_url):
    """
    Фикстура возвращает ссылку редиректа для логина и перехода к
    ссылке изменения
    """
    return f'{users_login_url}?next={news_edit_url}'


@pytest.fixture
def delete_redirect_url(users_login_url, news_delete_url):
    """
    Фикстура возвращает ссылку редиректа для логина и перехода к
    ссылке удаления
    """
    return f'{users_login_url}?next={news_delete_url}'
