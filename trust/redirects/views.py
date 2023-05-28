import requests
import os

from django.shortcuts import render, redirect
from dotenv import load_dotenv

from .forms import LinkForm

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
    response = ""#requests.get(url_send).json()
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


def user_get_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['activation_key']
            link = form.cleaned_data['URL_redirects']
            count_link = form.cleaned_data['URL_count']
            form.save()
            return redirect('/thank-you/')
        return render(request, 'index.html', {'form': form})
    form = LinkForm()
    return render(request, 'index.html', {'form': form}) 