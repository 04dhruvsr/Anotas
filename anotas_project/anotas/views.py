from django.shortcuts import render
from django.http import HttpResponse
from anotas.forms import CategoryForm,PageForm, UserForm,UserProfileForm, NoteForm, EditForm
from django.shortcuts import redirect
from django.urls import reverse
from anotas.models import Category, Page, Note, UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import time

def home(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['categories'] = category_list

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    request.session.set_test_cookie()

    return render(request, 'anotas/home.html', context=context_dict)

def about(request):
    context_dict = {}
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, 'anotas/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:       
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'anotas/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/anotas/')
        else:
            print(form.errors)
    return render(request, 'anotas/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if category is None:
        return redirect('/anotas/')
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('anotas:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'anotas/add_page.html', context=context_dict)

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'anotas/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('anotas:home'))
            else:
                return HttpResponse("Your anotas account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
        
    else:
        return render(request, 'anotas/login.html')
    
def user_page(request):
    context_dict = {}
    try:
        notes = Note.objects.filter(userID=request.user.get_username())
        print(request.user.get_username())
        print(Note.objects.filter(userID=request.user.get_username()))
        context_dict['notes'] = notes
    except Category.DoesNotExist:       
        context_dict['notes'] = None
    return render(request, 'anotas/user.html', context=context_dict)

def add_note(request):
    note_form = NoteForm()
    request.method = "POST"
    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            noteTitle = note_form.cleaned_data["noteTitle"]
            content = note_form.cleaned_data["content"]
            subject = note_form.cleaned_data["subject"]
            isPrivate = note_form.cleaned_data["isPrivate"]
            note = Note(noteTitle=noteTitle, content=content, subject=subject,isPrivate=isPrivate)
            note.set_fileName()
            note.set_userID(request)
            note.save()
                
            f = open(note.get_fileName(), "w")
            f.write(content)
        else:
            print("uh oh")
            print(note_form.errors)
    print(note_form.is_valid())
    return render(request, 'anotas/note_reader.html', {'note_form': note_form})

def note_editor(request, note_name_slug):
    context_dict = {}
    try:
        note = Note.objects.get(slug=note_name_slug.lower(), userID=request.user.get_username())
        f = open(note.get_fileName(), "r")
        context_dict["existing"] = f.readlines()
        context_dict["title"] = note.noteTitle
        print(f.readlines())
        print(note.get_fileName())
        f.close()
        edit_form = EditForm(request.POST)
        request.method = "POST"
        if request.method == "POST":
            if edit_form.is_valid():
                print(edit_form.cleaned_data)
                content = edit_form.cleaned_data["content"]
                f = open(note.get_fileName(), "w")
                f.write(content)
    except Note.DoesNotExist:
        context_dict['existing'] = None
        context_dict["title"] = None
    return render(request, "anotas/note_editor.html", context=context_dict)
        
        
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('anotas:home'))