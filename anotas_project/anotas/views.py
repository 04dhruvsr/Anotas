from django.shortcuts import render
from django.http import HttpResponse
from anotas.forms import CategoryForm,PageForm, UserForm,UserProfileForm, NoteForm, EditForm
from django.shortcuts import redirect
from django.urls import reverse
from anotas.models import Category, Page, Note, UserProfile, Subject
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import time

def home(request):
    subject_list = Subject.objects.order_by('-likes')[:5]
    context_dict = {}
    context_dict['subject'] = subject_list

    # context_dict['pages'] = page_list
    request.session.set_test_cookie()

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
def add_note(request, subject_name_slug):
    try:
        subject = Subject.objects.get(slug=subject_name_slug)
    except Subject.DoesNotExist:
        subject = None
    if subject is None:
        return redirect('/anotas/')
    form = NoteForm()
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            if subject:
                note = form.save(commit=False)
                note.subject = subject
                note.views = 0
                note.save()
                return redirect(reverse('anotas:show_subject', kwargs={'subject_name_slug': subject_name_slug}))
        else:
            print(form.errors)
    context_dict = {'form': form, 'subject': subject}
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
        title=original_note.title,
        content=original_note.content,
        old_owners = old_owners,
        userID = new_owner,
        copyCount = original_note.copyCount + 1,
    )

    new_note.save()

    return redirect('anotas:show_note', note_id=new_note.id)


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
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('anotas:home'))