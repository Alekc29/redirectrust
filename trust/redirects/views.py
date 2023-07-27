import datetime
import requests
import os

from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from dotenv import load_dotenv

from .forms import LinkForm, FeedbackForm
from .models import Connect, Stat 
import quickstart

load_dotenv()

API_KEY_UNISOFT = os.getenv('API_KEY_UNISOFT')
SEND_EMAIL = {1: os.getenv('SENDER_EMAIL'),
              2: os.getenv('SENDER_EMAIL_2'),
              3: os.getenv('SENDER_EMAIL_3'),
              4: os.getenv('SENDER_EMAIL_4'),
              5: os.getenv('SENDER_EMAIL_5'),}

INC = 1
LIMIT_LINK = 110


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
    template = 'redirects/unisender.html'
    stats = Stat.objects.get(donater=request.user)
    form = LinkForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        #code = form.cleaned_data['code']
        link = form.cleaned_data['link']
        count_link = form.cleaned_data['count_link']
        #form.save()
        if stats.balance <= 0:
            return render(request, template, {'form': form,
                                              'balance': stats.balance})
        body_header = (
            '<html>' +
            f'<body>{request.user}, здравствуйте!<br />'
        )
        global INC
        INC = 1
        if count_link > LIMIT_LINK:
            while count_link > LIMIT_LINK:
                count_link -= LIMIT_LINK
                body_footer = ''
                for i in range(1, LIMIT_LINK+1):
                    body_footer += f'<a href="{link}">список {i}</a><br />'
                body_footer += ('</body>' +
                                '</html>')
                body = body_header + body_footer
                url_send = (f'https://api.unisender.com/ru/api/sendEmail?format=json&' +
                            f'api_key={API_KEY_UNISOFT}&' +
                            f'email=Misterio <{SEND_EMAIL[INC]}>&' +
                            f'sender_name=UNISOFT&' +
                            f'sender_email={SEND_EMAIL[1]}&' +
                            f'subject=TRY_RED&' +
                            f'body={body}&' +
                            f'list_id=1&' +
                            f'lang=en&' +
                            f'track_read=0&' +
                            f'track_links=1&' +
                            f'error_checking=1&')
                requests.get(url_send)
                INC += 1
        if count_link <= LIMIT_LINK:
            body_footer = ''
            for i in range(1, count_link+1):
                body_footer += f'<a href="{link}">список {i}</a><br />'
            body_footer += ('</body>' +
                            '</html>')
            body = body_header + body_footer
            url_send = (f'https://api.unisender.com/ru/api/sendEmail?format=json&' +
                        f'api_key={API_KEY_UNISOFT}&' +
                        f'email=Misterio <{SEND_EMAIL[INC]}>&' +
                        f'sender_name=UNISOFT&' +
                        f'sender_email={SEND_EMAIL[1]}&' +
                        f'subject=TRY_RED&' +
                        f'body={body}&' +
                        f'list_id=1&' +
                        f'lang=en&' +
                        f'track_read=0&' +
                        f'track_links=1&' +
                        f'error_checking=1&')
            requests.get(url_send)
        stats.count_unisender += 1
        stats.save()
        return redirect('redirects:uni_result')
    return render(request, template, {'form': form,
                                      'balance': stats.balance})



def user_get_result(request):
    ''' Личный кабинет пользователя.
        Для получения редиректов. '''
    template = 'redirects/unisender_result.html'
    title = 'Личный кабинет.'
    response = ''
    count = 1
    for inc_main in range(1, INC+1):
        links = quickstart.main(inc_main)
    #links_2 = quickstart_2.main()
        for link in links:
            response += f'{count}: {link} \n'
            count += 1
    # for link_2 in links_2:
    #     response += f'{inc}: {link_2} \n'
    #     inc += 1
    # file = open(f"resp{request.user}.txt", "w")
    # file.write(response)
    # file.close()
    context = {
        'title': title,
        'page_obj': response,
    }
    return render(request, template, context)


def user_get_stats(request):
    ''' Личный кабинет пользователя.
        Для получения статистики. '''
    template = 'redirects/lk_stats.html'
    obj, created = Stat.objects.get_or_create(
        donater=request.user,
        defaults={
            'count_unisender': 0,
            'balance': 0,
            'donat': 0
        },
    )
    if obj.balance > 0:
        status = 'Active'
        now = datetime.datetime.now()
        check_date = datetime.timedelta(days=(round(obj.balance * 30 / 100))) + now
        date_active = f'Дейтсвует до {check_date.day}.{check_date.month}.{check_date.year}'
    else:
        status = 'InActive'
        date_active = 'Вы не можете использовать наш сервис.'
    title = 'Статистика.'
    context = {
        'title': title,
        'date_active': date_active,
        'status': status,
        'page_obj': obj,
    }
    return render(request, template, context)


def create_feedback(request):
    ''' Страница создания отзыва. '''
    template = 'redirects/create_feedback.html'
    form = FeedbackForm(
        request.POST or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.donater = request.user
        post.save()
        return redirect('redirects:thanks')
    return render(request, template, {'form': form})


class FeedbackThanks(TemplateView):
    template_name = 'redirects/feedback_thanks.html'