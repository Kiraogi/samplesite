from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.db.models import Q

from .models import AdvUser, SubRubric, Bb
from .forms import ProfileEditForm, RegisterForm, SearchForm
from .utilities import signer

"""
    rubric_bbs - функция-обработчик, 
    отображает объявления, относящиеся к рубрике, 
    с возможностью поиска
"""


def rubric_bbs(request, pk):
    rubric = get_object_or_404(SubRubric, pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=rubric)
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'rubric': rubric, 'page': page,
               'bbs': page.object_list, 'form': form}
    return render(request, 'main/rubric_bbs.html', context)


"""
    ProfileDeleteView - класс-обработчик, 
    предназначен для удаления пользовательской учетной записи
"""


class ProfileDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/profile_delete.html'
    success_url = reverse_lazy('main:index')
    success_message = 'Пользователь удален'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


"""
    user_activate - функция-обработчик, 
    активирует пользовательскую учетную запись
"""


def user_activate(request, sign):
    try:
        user = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/activation_failed.html')
    user = get_object_or_404(AdvUser, username=user)
    if user.is_activated:
        template = 'main/activation_done_earlier.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


"""
    RegisterDoneView - класс-обработчик, 
    отображает сообщение после регистрации
"""


class RegisterDoneView(TemplateView):
    template_name = 'main/register_done.html'


"""
    RegisterView - класс-обработчик, 
    регистрирует нового пользователя
"""


class RegisterView(CreateView):
    model = AdvUser
    template_name = 'main/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('main:register_done')


"""
    PasswordEditView - класс-обработчик, 
    меняет пароль зарегистрированного пользователя
"""


class PasswordEditView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_edit.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'


"""
    ProfileEditView - класс-обработчик, 
    изменяет профиль зарегистрированного пользователя
"""


class ProfileEditView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'main/profile_edit.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


"""
    BBLogoutView - класс-обработчик, 
    выполняет выход из системы
"""


class BBLogoutView(LogoutView):
    pass


"""
    profile - функция-обработчик, 
    отображает профиль зарегистрированного пользователя
"""


@login_required
def profile(request):
    bbs = Bb.objects.filter(author=request.user.pk)
    context = {'bbs': bbs}
    return render(request, 'main/profile.html', context)


"""
    BBloginView - класс-обработчик, 
    выполняет вход в систему
"""


class BBloginView(LoginView):
    template_name = 'main/login.html'


"""
    index - функция-обработчик, 
    отображает главную страницу
"""


def index(request):
    bbs = Bb.objects.filter(is_active=True).select_related('rubric')[:10]
    context = {'bbs': bbs}
    return render(request, 'main/index.html', context)


"""
    other_page - функция-обработчик, 
    отображает страницы, не относящиеся к объявлениям
"""


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


def bb_detail(request, rubric_pk, pk):
    bb = get_object_or_404(Bb, pk=pk)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/bb_detail.html', context)

@login_required
def profile_bb_detail(request, pk):
    bb = get_object_or_404(Bb, pk=pk, author=request.user)
    ais = bb.additionalimage_set.all()
    context = {'bb': bb, 'ais': ais}
    return render(request, 'main/bb_detail.html', context)
