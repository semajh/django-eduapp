from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponse
from testapp.forms import LoginForm, SignUpForm, CreateGroupForm, PostComment, CreateClassForm, CreateTimeChoice, \
    CreateQuestion
from django.contrib.auth.decorators import login_required
from testapp.models import Profile, Group, Comment, Classes, TimeChoice, Questions


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.username = form.cleaned_data.get('username')
            user.raw_password = form.cleaned_data.get('password1')
            user.is_mentor = form.cleaned_data.get('is_mentor')
            user.level = form.cleaned_data.get('level')
            user.save()
            user = authenticate(username=user.username, password=user.raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'testapp/signup.html', {'form': form})


def login_to_system(request):
    if request.method == 'POST':
        user = None
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    return render(request, 'testapp/login.html', {'form': form})


def index(request):
    return render(request, 'testapp/index.html')


@login_required
def home(request):
    context = {'form': CreateGroupForm(),
               'groups': Group.objects.all()}
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            group.refresh_from_db()
            group.name = form.cleaned_data.get('name')
            group.description = form.cleaned_data.get('description')
            group.attendees.add(Profile.objects.get(user=request.user))
            group.save()
            return render(request, 'testapp/home.html', context)
        else:
            return HttpResponse("The input is invalid")
    else:
        return render(request, 'testapp/home.html', context)


@login_required
def GroupView(request, group_id):
    group = Group.objects.get(id=group_id)
    comments = Group.objects.get(id=group_id).comments.order_by('-time')
    classes = group.classes.all()
    questions = group.questions.all()
    context = {'commentform': PostComment(),
               'classform': CreateClassForm(),
               'questionform': CreateQuestion(),
               'group': group,
               'comments': comments,
               'classes': classes,
               'questions': questions,
               'error': ''}
    if request.method == 'POST' and 'btnPostComment' in request.POST:
        form = PostComment(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            sender = request.user
            profile = Profile.objects.get(user=sender)
            comment = Comment(text=text, sender=profile)
            comment.save()
            group = Group.objects.get(id=group_id)
            group.comments.add(comment)
            group.save()
            return render(request, 'testapp/group.html', context)
        else:
            context['error'] = 'Invalid information'
            return render(request, 'testapp/group.html', context)
    elif request.method == 'POST' and 'btnJoinGroup' in request.POST:
        profile = Profile.objects.get(user=request.user)
        group = Group.objects.get(id=group_id)
        group.attendees.add(profile)
        group.save()
        return render(request, 'testapp/group.html', context)
    elif request.method == 'POST' and 'btnCreateClass' in request.POST:
        form = CreateClassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            aclass = Classes()
            aclass.name = name
            aclass.description = description
            aclass.save()
            group = Group.objects.get(id=group_id)
            group.classes.add(aclass)
            group.save()
            return render(request, 'testapp/group.html', context)
    elif request.method == 'POST' and 'btnCreateQuestion' in request.POST:
        form = CreateQuestion(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('question')
            description = form.cleaned_data.get('description')
            question = Questions()
            question.question = name
            question.description = description
            question.sender = Profile.objects.get(user=request.user)
            question.save()
            group = Group.objects.get(id=group_id)
            group.questions.add(question)
            group.save()
            return render(request, 'testapp/group.html', context)
        else:
            context['error'] = 'Invalid information'
            return render(request, 'testapp/group.html', context)

    else:
        return render(request, 'testapp/group.html', context)


@login_required
def ClassView(request, group_id, class_id):
    aclass = Classes.objects.get(id=class_id)
    profile = Profile.objects.get(user=request.user)
    comments = aclass.comments.order_by('-id')
    choices = aclass.times.all()
    context = {'class': aclass,
               'choices': choices,
               'comments': comments,
               'time_choice_form': CreateTimeChoice(),
               'form': PostComment(),
               'profile': profile,
               'error': ''}

    if request.method == 'POST':
        if 'btnJoinClass' in request.POST:
            aclass.attendees.add(profile)
            aclass.save()
            return render(request, 'testapp/class.html', context)
        elif 'btnVote' in request.POST:
            timechoice = TimeChoice.objects.get(id=int(request.POST.get('btnVote')))
            timechoice.votes += 1
            timechoice.save()
            return render(request, 'testapp/class.html', context)
        elif 'btnCreateChoice' in request.POST:
            form = CreateTimeChoice(request.POST)
            if form.is_valid():
                start = form.cleaned_data.get('start')
                duration = form.cleaned_data.get('duration')
                choice = TimeChoice()
                choice.start = start
                choice.duration = duration
                choice.votes = 0
                choice.save()
                aclass.times.add(choice)
                aclass.save()
                return render(request, 'testapp/class.html', context)
            else:
                context['error'] = 'Invalid information'
                return render(request, 'testapp/class.html', context)
        elif 'btnPostComment' in request.POST:
            form = PostComment(request.POST)
            if form.is_valid():
                text = form.cleaned_data.get('text')
                sender = request.user
                profile = Profile.objects.get(user=sender)
                comment = Comment(text=text, sender=profile)
                comment.save()
                aclass = Classes.objects.get(id=class_id)
                aclass.comments.add(comment)
                aclass.save()
                return render(request, 'testapp/class.html', context)
            else:
                context['error'] = 'Invalid information'
                return render(request, 'testapp/class.html', context)

    else:
        return render(request, 'testapp/class.html', context)


def LogoutView(request):
    logout(request)
    return redirect("index")
