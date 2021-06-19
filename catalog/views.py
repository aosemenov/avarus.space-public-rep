from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.db import transaction
from django.http import HttpResponse, request
from .models import Book, Author, BookInstance, FeedBack
from django.shortcuts import render, redirect
from .forms import FeedBackForm
from django.views.generic import View
from django.contrib import messages
from django.conf import settings
from mysite import settings
from django.views import generic
from .forms import UserEditForm, ProfileEditForm




def index(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile details updated.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'catalog/index.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})

    return render(request,
                  'catalog/index.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})



def AboutView(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST.getlist('email')
        message = request.POST.get('message')
        send_mail(f'Обратная связь от {username}',
                  f'{ message }.\nEmail: {email}',
                  settings.EMAIL_HOST_USER, ['vitalii.zemlianskii@ieu.uzh.ch', 'moose.2000@mail.ru', 'diankina@gmail.com'])
    return render(request, 'catalog/about.html')

def DatasetsView(request):
    bookinstance_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('book')
    book_list = Book.objects.filter(status='pu')
    return render(request, 'catalog/bookinstance_list_borrowed_user.html', {'book_list': book_list, 'bookinstance_list':bookinstance_list})



class BookDetailView(generic.DetailView):
    model = Book


from django.contrib.auth.mixins import LoginRequiredMixin




class LoanedBooksAllListView(generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('book')


class RequestsByUserListView(LoginRequiredMixin, generic.ListView):
    model = FeedBack
    template_name = 'catalog/datasets_requests.html'

    def get_queryset(self):
        return FeedBack.objects.filter(customer_login=self.request.user).order_by('name_space')


# FEED BACK
from django.conf import settings


class FeedBackView(View):
    def post(self, request):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            form.save()
            user = request.POST.get('customer_login')
            position = request.POST.get('position')
            organization = request.POST.get('organization')
            to = request.POST.get('email')
            name_space = request.POST.get('name_space')
            description = request.POST.get('description')
            messages.success(request, 'The request was sent successfully')
            send_mail(f'avarus.space от {user}', f'Запрос на доступ к {name_space} от {user} {organization} {position}.\nЦель запроса: {description}.\nEmail: {to}', settings.EMAIL_HOST_USER, ['vitalii.zemlianskii@ieu.uzh.ch', 'moose.2000@mail.ru', 'diankina@gmail.com'])
            return render(request, 'catalog/index.html')
        else:
            form = FeedBackForm()
            messages.success(request, 'Error form')
            return render(request, 'catalog/index.html')


# СТАТИСТИКА АНАЛИТИКА


from django.shortcuts import render
from .R import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Book, BookInstance
from django.views.generic import View


def analysis_view(request):
    if request.user.is_authenticated:
        return render(request, 'R/analysis.html')


def StatisticsDatasetsView(request):
    bookinstance_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('book')
    book_list = Book.objects.filter(status='pu')
    return render(request, 'catalog/statistics.html', {'book_list': book_list, 'bookinstance_list': bookinstance_list})

def FactorDatasetsView(request):
    bookinstance_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('book')
    book_list = Book.objects.filter(status='pu')
    return render(request, 'R/factor.html', {'book_list': book_list, 'bookinstance_list': bookinstance_list})

def CompDatasetsView(request):
    bookinstance_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('book')
    book_list = Book.objects.filter(status='pu')
    return render(request, 'R/comp.html', {'book_list': book_list, 'bookinstance_list': bookinstance_list})

def JacquardDatasetsView(request):
    bookinstance_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('book')
    book_list = Book.objects.filter(status='pu')
    return render(request, 'R/jaccar.html', {'book_list': book_list, 'bookinstance_list': bookinstance_list})

def CorDatasetsView(request):
    bookinstance_list = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('book')
    book_list = Book.objects.filter(status='pu')
    return render(request, 'R/cor.html', {'book_list': book_list, 'bookinstance_list': bookinstance_list})


class DatasetDetailView(generic.DetailView):
    model = BookInstance

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o')


def get_name_comp(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        columns = request.POST.getlist('columns')
        length = str(len(columns))
        some_result = module_comp(datasets, length, columns)
        print(datasets, length, columns)
        import shutil
        source = 'Rplots.pdf'
        dest = 'media/Rplots.pdf'
        try:
            dest = shutil.move(source, dest)
            print("File is moved successfully to: ", dest)
        except IsADirectoryError:
            print("Source is a file but destination is a directory.")
        except NotADirectoryError:
            print("Source is a directory but destination is a file.")
        except PermissionError:
            print("Operation not permitted.")
        except OSError as error:
            print(error)
        print('The file is successfully moved to another destination')
        request.session['result'] = some_result
        return render(request, template_name='R/comp_result.html', context={'result': request.session['result']})
    else:
        return render(request, 'R/comp_column.html')


def get_name(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        columns = request.POST.getlist('columns')
        some_result = module(datasets, columns)
        request.session['result'] = some_result
        return render(request, template_name='R/cor_result.html', context={'result': request.session['result']})
    else:
        return render(request, 'R/cor_column.html')


def get_column_statistics(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        datasets = datasets.split()
        ds_1 = datasets[0]
        ds_2 = datasets[1]
        print(ds_1, ds_2)
        some_result = module_col_statistics(ds_1)
        some_result_env = module_col_statistics_env(ds_2)
        request.session['result_column'] = some_result
        request.session['result_column_env'] = some_result_env
        request.session['chosen_dataset'] = ds_1
        request.session['chosen_dataset_env'] = ds_2

        return render(request, template_name='catalog/statistics_column.html', context={
            'result_column': request.session['result_column'],
            'result_column_env': request.session['result_column_env'],
            'chosen_dataset': request.session['chosen_dataset'],
            'chosen_dataset_env': request.session['chosen_dataset_env']})
    else:
        return render(request, 'catalog/statistics.html')


def get_name_statistics(request):
    if request.method == 'POST':
        ds_1 = request.POST['dataset']
        ds_2 = request.POST['dataset_env']
        columns = request.POST.getlist('columns')
        columns_env = request.POST.getlist('columns_env')
        print(columns, columns_env, ds_1, ds_2)
        length = str(len(columns))
        length_env = str(len(columns_env))
        some_result = module_statistics(ds_1, length, columns)
        some_result_env = module_statistics_env(ds_2, length_env, columns_env)
        import shutil
        source = 'subset.xlsx'
        dest = 'media/subset.xlsx'
        try:
            dest = shutil.move(source, dest)
            print("File is moved successfully to: ", dest)
        except IsADirectoryError:
            print("Source is a file but destination is a directory.")
        except NotADirectoryError:
            print("Source is a directory but destination is a file.")
        except PermissionError:
            print("Operation not permitted.")
        except OSError as error:
            print(error)
        print('The file is successfully moved to another destination')

        source = 'subset_env.xlsx'
        dest = 'media/subset_env.xlsx'
        try:
            dest = shutil.move(source, dest)
            print("File is moved successfully to: ", dest)
        except IsADirectoryError:
            print("Source is a file but destination is a directory.")
        except NotADirectoryError:
            print("Source is a directory but destination is a file.")
        except PermissionError:
            print("Operation not permitted.")
        except OSError as error:
            print(error)
        print('The file is successfully moved to another destination')
        request.session['result'] = some_result
        request.session['result_env'] = some_result_env
        return render(request, template_name='catalog/statistics_result.html', context={'result': request.session['result'],
                                                                                        'result_env': request.session[
                                                                                            'result_env']})
    else:
        return render(request, 'catalog/statistics_column.html')


def get_column(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        some_result = module_col(datasets)
        request.session['result_column'] = some_result
        request.session['chosen_dataset'] = datasets
        return render(request, template_name='R/cor_column.html', context={
            'result_column': request.session['result_column'],
            'chosen_dataset': request.session['chosen_dataset']})
    else:
        return render(request, 'R/cor.html')


def get_column_comp(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        some_result = module_col_comp(datasets)
        request.session['result_column'] = some_result
        request.session['chosen_dataset'] = datasets
        return render(request, template_name='R/comp_column.html', context={
            'result_column': request.session['result_column'],
            'chosen_dataset': request.session['chosen_dataset']})
    else:
        return render(request, 'R/comp.html')

def get_column_factor(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        some_result = module_col_factor(datasets)
        request.session['result_column'] = some_result
        request.session['chosen_dataset'] = datasets
        return render(request, template_name='R/factor_column.html', context={
            'result_column': request.session['result_column'],
            'chosen_dataset': request.session['chosen_dataset']})
    else:
        return render(request, 'R/factor.html')


def get_name_factor(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        columns = request.POST.getlist('columns')
        length = str(len(columns))
        some_result = module_factor(datasets, length, columns)
        request.session['result'] = some_result
        return render(request, template_name='R/factor_result.html', context={'result': request.session['result']})
    else:
        return render(request, 'R/factor_column.html')

def get_name_jacquard(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        some_result = module_jacquard(datasets)
        import shutil
        source = 'Jaccard.pdf'
        dest = 'media/Jaccard.pdf'
        try:
            dest = shutil.move(source, dest)
            print("File is moved successfully to: ", dest)
        except IsADirectoryError:
            print("Source is a file but destination is a directory.")
        except NotADirectoryError:
            print("Source is a directory but destination is a file.")
        except PermissionError:
            print("Operation not permitted.")
        except OSError as error:
            print(error)
        print('The file is successfully moved to another destination')
        request.session['result'] = some_result
        return render(request, template_name='R/jaccar_result.html', context={'result': request.session['result']})
    else:
        return render(request, 'R/jaccar.html')


def get_name_plants(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        some_result = module_plants(datasets)
        request.session['result'] = some_result
        return render(request, template_name='R/species_amount_result.html', context={'result': request.session['result']})
    else:
        return render(request, 'R/statistics.html')


def get_name_species(request):
    if request.method == 'POST':
        datasets = request.POST['dataset']
        group = request.POST['group']
        some_result = module_species(datasets, group)
        import shutil
        source = 'Rplots.pdf'
        dest = 'media/Rplots.pdf'
        try:
            dest = shutil.move(source, dest)
            print("File is moved successfully to: ", dest)
        except IsADirectoryError:
            print("Source is a file but destination is a directory.")
        except NotADirectoryError:
            print("Source is a directory but destination is a file.")
        except PermissionError:
            print("Operation not permitted.")
        except OSError as error:
            print(error)
        print('The file is successfully moved to another destination')
        request.session['result'] = some_result
        return render(request, template_name='R/groups_amount_result.html', context={'result': request.session['result']})
    else:
        return render(request, 'R/statistics.html')
