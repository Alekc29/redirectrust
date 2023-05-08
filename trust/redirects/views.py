import requests
import os

from django.shortcuts import render
from dotenv import load_dotenv

load_dotenv()

API_KEY_UNISOFT = os.getenv('API_KEY_UNISOFT')
SEND_EMAIL = os.getenv('SENDER_EMAIL')


def index(request):
    ''' Главная страница. '''
    template = 'redirects/index.html'
    title = 'Последние обновления на сайте'
    body = ('<html>' +
            '<head>' +
                '<title></title>' +
            '</head>' +
            '<body>Дмитрий, здравствуйте!<br />' +
            '<br />' +
            'Подготовили для вас информацию, просим ознакомиться:<br />' +
            '<a href="https://ip2geolocation.com/?ip=rambler.ru">список 1</a><br />' +
            '</body>' +
            '</html>')
    url_test = (f'https://api.unisender.com/ru/api/sendEmail?format=json&' +
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
    response = requests.get(url_test).json()
    page_obj = 'Пусто однако'
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