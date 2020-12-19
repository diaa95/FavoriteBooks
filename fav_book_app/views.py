from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    errors = models.User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_id = models.registration(request.POST)
        messages.success(request, "user successfully Logged in/Registered")
        request.session['logged_id'] = user_id
        return redirect(f"success/{user_id}")


def log_in(request):
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        context = models.log_in(request.POST)
        if context['flag']:
            request.session['logged_id'] = context['this_user'].id
            messages.success(request, "You Registered/Logged in Successfully")
            return redirect(f"success/{context['this_user'].id}")
        else:
            messages.error(request, "you need to register")
            return redirect("/")


def success(request, user_id):
    user = models.success(user_id)
    if request.session['logged_id'] == user['this_user'].id:
        return render(request, 'fav_book.html', user)
    else:
        return redirect('/')


def user_page(request, user_id):
    context = {
        'this_user': models.get_user(user_id)
    }
    return render(request, "YourFavorites.html", context)


def add_book(request, user_id):
    errors = models.Book.objects.add_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/success/{user_id}")
    else:
        models.add_book(user_id, request.POST)
        return redirect(f'/success/{user_id}')


def book_details(request, user_id, book_id):
    if int(book_id) in models.uploaded(user_id):
        return redirect(f"/edit/{book_id}/{user_id}")
    else:
        return redirect(f"/display/{book_id}/{user_id}")


def edit(request, book_id, user_id):
    context = {
        'this_book': models.get_book(book_id),
        "this_user": models.get_user(user_id)
    }
    return render(request, 'edit.html', context)


def update(request, book_id, user_id):
    errors = models.Book.objects.add_book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/success/{user_id}")
    else:
        models.update(request.POST, book_id)
        return redirect(f'/success/{user_id}')


def destroy(request, book_id, user_id):
    models.destroy(book_id)
    return redirect(f'/success/{user_id}')



def display(request, book_id, user_id):
    context = models.display(book_id, user_id)
    return render(request, "display.html", context)


def add_fav(request, book_id, user_id):
    models.add_fav(book_id, user_id)
    return redirect(f'/success/{user_id}')


def unfavorite(request, book_id, user_id):
    models.unfavorite(book_id, user_id)
    return redirect(f'/success/{user_id}')


def log_out(request):
    del request.session['logged_id']
    return redirect('/')