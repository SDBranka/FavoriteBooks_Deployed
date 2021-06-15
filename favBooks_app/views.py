from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book
from django.contrib import messages


# Create your views here.

def index(request):
    if not 'user_id' in request.session:
        return redirect("/")

    logged_user = User.objects.get(id=request.session['user_id'])
    context = {
        "logged_user": logged_user,
        "all_books": Book.objects.all()
    }
    return render(request, "books_index.html", context)

def add_book(request):
    if not 'user_id' in request.session:
        return redirect("/")

    if request.method == "POST":
        
        errors = Book.objects.add_book_validator(request.POST)
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
            return redirect("/books")

        logged_user = User.objects.get(id=request.session['user_id'])
        new_book = Book.objects.create(
            uploaded_by = logged_user,
            title = request.POST['title'],
            desc = request.POST['desc']
        )
        new_book.favorited_by.add(logged_user)
    return redirect("/books")

def add_to_fav(request):
    if not 'user_id' in request.session:
        return redirect("/")

    if request.method == "POST":
        logged_user = User.objects.get(id= request.session['user_id'])
        book_to_fav = Book.objects.get(id= request.POST['book_id'])
        book_to_fav.favorited_by.add(logged_user)
    return redirect(f"/books/{ request.POST['book_id'] }")

def view_book(request, book_id):
    if not 'user_id' in request.session:
        return redirect("/")

    logged_user = User.objects.get(id= request.session['user_id'])
    book = Book.objects.get(id=book_id)
    book_uploader = book.uploaded_by
    context = {
            "logged_user": logged_user,
            "book": book,
        }
    if book_uploader == logged_user:
        return render(request, "edit_book.html", context)
    else:
        return render(request, "display_book.html", context)

def edit(request):
    if not 'user_id' in request.session:
        return redirect("/")

    if request.method == "POST":
        errors = Book.objects.edit_book_validator(request.POST)
        if len(errors) > 0:
            for error in errors.values():
                messages.error(request, error)
        else:
            book_to_edit = Book.objects.get(id=request.POST['book_id'])
            book_to_edit.title = request.POST['title']
            book_to_edit.desc = request.POST['desc']
            book_to_edit.save()
    return redirect(f"/books/{ request.POST['book_id'] }")

def check_destroy(request, book_id):
    if not 'user_id' in request.session:
        return redirect("/")

    context = {
        "book_to_destroy": Book.objects.get(id=book_id)
    }
    return render(request, "check_destroy.html", context)
    
def destroy(request):
    if not 'user_id' in request.session:
        return redirect("/")

    if request.method == "POST":
        book_to_destroy = Book.objects.get(id=request.POST['book_id'])
        book_to_destroy.delete()
    return redirect("/books")

def unfavorite(request, book_id):
    if not 'user_id' in request.session:
        return redirect("/")

    book_to_unfav = Book.objects.get(id=book_id)
    logged_user = User.objects.get(id = request.session['user_id'])
    book_to_unfav.favorited_by.remove(logged_user)
    return redirect(f"/books/{book_id}")

def user_favorites(request):
    if not 'user_id' in request.session:
        return redirect("/")
    
    context = {
        "logged_user": User.objects.get(id = request.session['user_id'])
    }
    return render(request, "user_favorites.html", context)


















