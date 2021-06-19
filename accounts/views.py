from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from django.utils.translation import gettext as _
from catalog.models import AddLocations
from json import dumps

def registerPage(request):

    global context
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username', 'email')
                return redirect('login')
            else:
                if len(form.cleaned_data.get('password1')) < 5:
                    message = _("Password must be more than 5 symbols!")
                    form = CreateUserForm()
                    context = {'form': form, 'message': message}
                else:
                    message_error = _("The passwords are different!")
                    form = CreateUserForm()
                    context = {'form': form, 'message_error': message_error}
                return render(request, 'accounts/register.html', context)


        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Username OR password is incorrect'
                form = CreateUserForm()
                context = {'form': form, 'message': message}
                return render(request, 'accounts/login.html', context)

        context = {}
        return render(request, 'accounts/login.html', context)


def passwordPage(request):
    context = {}
    return render(request, 'accounts/password_reset_confirm.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    new_place = AddLocations.objects.all()

    data = [{}]
    for i in range(new_place.count()):
        place = {
        "center": [float(new_place[i].latitude), float(new_place[i].longitude)],
        "name": f"{new_place[i].num}. {new_place[i].name} ({new_place[i].authors})",
        "ContentHeader":[f"<a>{new_place[i].name}</a><br><span class='description'>{new_place[i].authors}</span><hr class='hr1'/>"],
        "ContentBody": [f"<a>Location Map</a><br/><img src='../media/pictures/{new_place[i].url_photo}' height='150' width='200'><br/><br/><a id='btn-preview' type='button' class='btn btn-info'  href={ new_place[i].url_page } style='color:white;'>Open</a>"],
        "ContentFooter": [f"Number of Plots:<br/>{new_place[i].plots}"],
        "hint": [f"<div class='map__hint'>{new_place[i].name}</div>"]
        }
        data.insert(0, place)

    jsondata = dumps(data)
    return render(request, 'object_list.html', {'json_data': jsondata})
