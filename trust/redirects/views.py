import requests
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from dotenv import load_dotenv

from .forms import LinkForm
from quickstart import main

load_dotenv()

API_KEY_UNISOFT = os.getenv('API_KEY_UNISOFT')
SEND_EMAIL = os.getenv('SENDER_EMAIL')


def index(request):
    ''' Главная страница. '''
    template = 'redirects/index.html'
    title = 'Последние обновления на сайте'
    response = 'Контента нетю.'
    context = {
        'title': title,
        'page_obj': response,
    }
    return render(request, template, context)


def index_en(request):
    ''' Главная страница на английском. '''
    template = 'redirects/index_en.html'
    title = 'Последние обновления на сайте'
    page_obj = 'Пусто однако'
    context = {
        'title': title,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def user_get_link(request):
    ''' Личный кабинет пользователя.
        Заполняет поля кода, ссылки и число. '''
    template = 'redirects/office.html'
    form = LinkForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        code = form.cleaned_data['code']
        link = form.cleaned_data['link']
        count_link = form.cleaned_data['count_link']
        #form.save()
        if code != f'code_{request.user}':
            return render(request, template, {'form': form})
        body_header = (
            '<html>' +
            '<head>' +
            '<title></title>' +
            '</head>' +
            f'<body>{request.user}, здравствуйте!<br />' +
            '<br />' +
            'Подготовили для вас информацию, просим ознакомиться:<br />'
        )
        body_footer = ''
        for i in range(1, count_link+1):
            body_footer += f'<a href="{link}">список {i}</a><br />'
        body_footer += ('</body>' +
                        '</html>')
        body = body_header + body_footer
        url_send = (f'https://api.unisender.com/ru/api/sendEmail?format=json&' +
                    f'api_key={API_KEY_UNISOFT}&' +
                    f'email=Misterio <{SEND_EMAIL}>&' +
                    f'sender_name=UNISOFT&' +
                    f'sender_email={SEND_EMAIL}&' +
                    f'subject=TRY_RED&' +
                    f'body={body}&' +
                    f'list_id=1&' +
                    f'lang=en&' +
                    f'track_read=0&' +
                    f'track_links=1&' +
                    f'error_checking=1&')
        requests.get(url_send)
        return redirect('redirects:result')
    return render(request, template, {'form': form})


def user_get_result(request):
    ''' Личный кабинет пользователя.
        Для получения редиректов. '''
    template = 'redirects/office_result.html'
    title = 'Личный кабинет.'
    links = main()
    response = ''
    for link in links:
        response += link
    context = {
        'title': title,
        'page_obj': response,
    }
    return render(request, template, context)