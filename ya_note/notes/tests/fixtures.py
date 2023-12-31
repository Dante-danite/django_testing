from django.urls import reverse

SLUG = 'slug'

URL_NOTES_ADD = reverse('notes:add')
URL_NOTES_LIST = reverse('notes:list')
URL_NOTES_EDIT = reverse('notes:edit', args=(SLUG,))
URL_NOTES_DELETE = reverse('notes:delete', args=(SLUG,))
URL_NOTES_SUCCESS = reverse('notes:success')
URL_NOTES_HOME = reverse('notes:home')
URL_NOTES_DETAIL = reverse('notes:detail', args=(SLUG,))

URL_USERS_LOGIN = reverse('users:login')
URL_USERS_LOGOUT = reverse('users:logout')
URL_USERS_SIGNUP = reverse('users:signup')

URL_REDIRECT_ADD = f'{URL_USERS_LOGIN}?next={URL_NOTES_ADD}'
URL_REDIRECT_SUCCESS = f'{URL_USERS_LOGIN}?next={URL_NOTES_SUCCESS}'
URL_REDIRECT_LIST = f'{URL_USERS_LOGIN}?next={URL_NOTES_LIST}'
URL_REDIRECT_DETAIL = f'{URL_USERS_LOGIN}?next={URL_NOTES_DETAIL}'
URL_REDIRECT_EDIT = f'{URL_USERS_LOGIN}?next={URL_NOTES_EDIT}'
URL_REDIRECT_DELETE = f'{URL_USERS_LOGIN}?next={URL_NOTES_DELETE}'

REDIRECTS_ANONYM = (
    (URL_NOTES_LIST, URL_REDIRECT_LIST),
    (URL_NOTES_SUCCESS, URL_REDIRECT_SUCCESS),
    (URL_NOTES_ADD, URL_REDIRECT_ADD),
    (URL_NOTES_DETAIL, URL_REDIRECT_DETAIL),
    (URL_NOTES_EDIT, URL_REDIRECT_EDIT),
    (URL_NOTES_DELETE, URL_REDIRECT_DELETE),
)

PUBLIC_URLS = (
    URL_NOTES_HOME,
    URL_USERS_LOGIN,
    URL_USERS_SIGNUP,
    URL_USERS_LOGOUT,
)

ONLY_AUTH_URLS = (
    URL_NOTES_LIST,
    URL_NOTES_SUCCESS,
    URL_NOTES_ADD,
)
AUTHOR_URLS = (
    URL_NOTES_DETAIL,
    URL_NOTES_EDIT,
    URL_NOTES_DELETE,
)

FORM_URLS = [
    URL_NOTES_EDIT, URL_NOTES_ADD
]
