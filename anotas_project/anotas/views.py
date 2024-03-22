from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from anotas.forms import NoteForm, SubjectForm, UserProfileForm, UserForm
from django.shortcuts import redirect
from django.urls import reverse
from anotas.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import os

def home(request):
    subject_list = Subject.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['subject'] = subject_list
    #context_dict['pages'] = page_list

    return render(request, 'anotas/home.html', context=context_dict)

def about(request):
    context_dict = {}
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    return render(request, 'anotas/about.html', context=context_dict)

def show_subject(request, subject_name_slug):
    context_dict = {}
    try:
        subject = Subject.objects.get(slug=subject_name_slug)
        pages = Page.objects.filter(subject=subject)
        context_dict['pages'] = pages
        context_dict['subject'] = subject
    except Subject.DoesNotExist:       
        context_dict['subject'] = None
        context_dict['pages'] = None
    return render(request, 'anotas/subject.html', context=context_dict)

@login_required
def add_subject(request):
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/anotas/')
        else:
            print(form.errors)
    return render(request, 'anotas/add_subject.html', {'form': form})

@login_required
def add_note(request):
    """try:

        subject = Subject.objects.get(slug=subject_name_slug)
    except Subject.DoesNotExist:
        subject = None
    if subject is None:
        return redirect('/anotas/')"""
    form = NoteForm()
    sub_form = SubjectForm()
    request.method = "POST"

    if request.method == 'POST':
        form = NoteForm(request.POST)
        sub_form = SubjectForm(request.POST)
        if form.is_valid():

            note = form.save(commit=False)
            note.views = 0
            note.userID = get_object_or_404(UserProfile, user=request.user)
            note.save()
            print(note.noteTitle)
            f = open(note.fileName, "w")
            f.write("")
            return redirect(reverse('anotas:note_editor', kwargs={'note_name_slug': note.noteTitle}))
        elif sub_form.is_valid():
            subject = sub_form.save()
            subject.save()
    
    context_dict = {'form': form, "sub_form": sub_form}
    return render(request, 'anotas/note_reader.html', context=context_dict)

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

@login_required
def copy_note(request, note_id):
    original_note = get_object_or_404(Note, id=note_id)
    
    old_owners = original_note.past_owners
    old_owners = old_owners.my_char_field

    previous_owner = get_object_or_404(UserID,original_note.userID).username
    # new_owner.username
    while len(old_owners+" "+ previous_owner)>255:
        old_owners = old_owners.split(" ")
        old_owners = old_owners[1:]
        old_owners = " ".join(old_owners)
    old_owners = old_owners+ " " + previous_owner

    new_owner = request.user
    new_note = Note(
        subject=original_note.subject,
        title=original_note.noteTitle + "_copy by_" + str(request.user),
        old_owners = old_owners,
        userID = new_owner,
        copyCount = original_note.copyCount + 1,
    )

    new_note.save()

    return redirect('anotas:show_note', note_id=new_note.id)

def user_page(request):
    context_dict = {}
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        notes = Note.objects.filter(userID = user_profile.id)
        print(user_profile)
        print(notes)
        context_dict['notes'] = notes
    except UserProfile.DoesNotExist:       
        context_dict['notes'] = None
    return render(request, 'anotas/user.html', context=context_dict)


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

@login_required
def note_editor(request, note_name_slug): #TODO doesnt read yet
    context_dict = {}
    try:
        note = Note.objects.get(slug=note_name_slug.lower())
        local_path = os.path.dirname(__file__)
        print(local_path)
        local_path = local_path[:-6]
        print(local_path)
        f = open(local_path + note.fileName, "r")
        text = ""
        for line in f.readlines():
            text += line + " "
        print(text)
        context_dict["title"] = note.noteTitle
        print(f.readlines())
        print(note.fileName)
        context_dict["text"] = text
        f.close()
    except Note.DoesNotExist:
        context_dict['text'] = None
        context_dict["title"] = None
    print(text)
    return render(request, "anotas/note_editor.html", context=context_dict)

def search_results(request):
    if request.method == "POST":
        user_search= request.POST["user_search"]
        print(user_search)
        notes= Note.objects.filter(noteTitle__contains= user_search)
        subjects= Subject.objects.filter(name__contains= user_search)
        return render(request, 'anotas/search_results.html', {"user_search": user_search, "notes": notes, "subjects": subjects})
    else:
        return render(request, 'anotas/search_results.html')
    
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('anotas:home'))