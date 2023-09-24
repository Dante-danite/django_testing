from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects
from pytest_lazyfixture import lazy_fixture

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, user, status', ((lazy_fixture('users_signup_url'),
                           pytest.lazy_fixture('admin_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('users_login_url'),
                           pytest.lazy_fixture('admin_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('users_logout_url'),
                           pytest.lazy_fixture('admin_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('news_home_url'),
                           pytest.lazy_fixture('admin_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('news_detail_url'),
                           pytest.lazy_fixture('admin_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('news_edit_url'),
                           pytest.lazy_fixture('admin_client'),
                           HTTPStatus.NOT_FOUND),

                          (lazy_fixture('news_delete_url'),
                           pytest.lazy_fixture('admin_client'),
                           HTTPStatus.NOT_FOUND),

                          (lazy_fixture('users_signup_url'),
                           pytest.lazy_fixture('author_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('users_login_url'),
                           pytest.lazy_fixture('author_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('users_logout_url'),
                           pytest.lazy_fixture('author_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('news_home_url'),
                           pytest.lazy_fixture('author_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('news_detail_url'),
                           pytest.lazy_fixture('author_client'),
                           HTTPStatus.OK),

                          (lazy_fixture('news_edit_url'),
                           pytest.lazy_fixture('author_client'),
                           HTTPStatus.OK),

                          (pytest.lazy_fixture('news_delete_url'),
                           pytest.lazy_fixture('author_client'),
                           HTTPStatus.OK),

                          (pytest.lazy_fixture('users_signup_url'),
                           pytest.lazy_fixture('client'),
                           HTTPStatus.OK),

                          (pytest.lazy_fixture('users_login_url'),
                           pytest.lazy_fixture('client'),
                           HTTPStatus.OK),

                          (pytest.lazy_fixture('users_logout_url'),
                           pytest.lazy_fixture('client'),
                           HTTPStatus.OK),

                          (pytest.lazy_fixture('news_home_url'),
                           pytest.lazy_fixture('client'),
                           HTTPStatus.OK),

                          (pytest.lazy_fixture('news_detail_url'),
                           pytest.lazy_fixture('client'),
                           HTTPStatus.OK),

                          (pytest.lazy_fixture('news_edit_url'),
                           pytest.lazy_fixture('client'),
                           HTTPStatus.FOUND),

                          (pytest.lazy_fixture('news_delete_url'),
                           pytest.lazy_fixture('client'),
                           HTTPStatus.FOUND),
                          )
)
def test_overall_availability(
        url, user, status
):
    """
    Главная страница доступна анонимному пользователю

    Страница отдельной новости доступна анонимному пользователю

    Страницы удаления и редактирования комментария доступны автору комментария

    При попытке перейти на страницу редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации

    Проверка что авторизированный пользователь (admin_client) не может
    зайти на страницу редактирования и удаления (возвращается ошибка 404)

    Тесты для проверки доступности анонимному пользователю (client)

    Страницы регистрации пользователей, входа в учётную запись
    и выхода из неё доступны анонимным пользователям
    """
    response = user.get(url)

    assert response.status_code == status


@pytest.mark.parametrize(
    'url, redirect_url',
    ((pytest.lazy_fixture('news_edit_url'),
      pytest.lazy_fixture('edit_redirect_url')),
     (pytest.lazy_fixture('news_edit_url'),
      pytest.lazy_fixture('edit_redirect_url')),
     (pytest.lazy_fixture('news_edit_url'),
      pytest.lazy_fixture('edit_redirect_url')),
     (pytest.lazy_fixture('news_delete_url'),
      pytest.lazy_fixture('delete_redirect_url')),
     ),
)
def test_redirects_for_anonymous_client(client, url, redirect_url):
    """
    При попытке перейти на страницу редактирования или удаления комментария
    анонимный пользователь перенаправляется на страницу авторизации
    """
    assertRedirects(client.get(url), redirect_url)


@pytest.mark.parametrize(
    'url, user, redirect_url, form_data_to_send',
    ((pytest.lazy_fixture('news_detail_url'),
      pytest.lazy_fixture('client'),
      pytest.lazy_fixture('news_detail_redirect_url'),
      pytest.lazy_fixture('form_data'),
      ),

     (lazy_fixture('news_detail_url'),
      pytest.lazy_fixture('author_client'),
      lazy_fixture('news_comment_redirect'),
      lazy_fixture('form_data'),
      ),
     (lazy_fixture('news_edit_url'),
      pytest.lazy_fixture('author_client'),
      lazy_fixture('news_comment_redirect'),
      lazy_fixture('form_data'),

      ),
     (lazy_fixture('news_delete_url'),
      pytest.lazy_fixture('author_client'),
      lazy_fixture('news_comment_redirect'),
      None,
      ),

     ))
def test_redirect_post_requests(user, url, redirect_url, form_data_to_send):
    """Проверка редиректов при POST запросах"""
    assertRedirects(user.post(url, data=form_data_to_send), redirect_url)
