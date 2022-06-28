from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
import datetime
import json
import re

from .models import *
from .extras.functions import *
from .extras.forms import *

# Views for the WebAid app

# Home page view
def index(request):
    # Pass most recent opportunities
    opportunities = Opportunity.get_latest(5)

    # Pass three top helpers
    helpers = User.objects.all().annotate(res_count=models.Count('resolved')).exclude(res_count=0).order_by('-res_count')[:3]

    return render(request, 'WebAid/index.html', {
        'opportunities': opportunities,
        'helpers': helpers
    })


def login_view(request):
    next = request.GET.get('next'.replace('/', ''), None)
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if next:
                next = reverse(next)
            else:
                next = reverse("user", kwargs={'user_id':request.user.id})
            return HttpResponseRedirect(next)
        else:
            return render(request, "WebAid/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "WebAid/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        location = request.POST["location"]
        skills = request.POST["skills"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "WebAid/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.location = location
            user.skills = skills
            user.save()
        except IntegrityError:
            return render(request, "WebAid/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("user", kwargs={'user_id':request.user.id}))
    else:
        return render(request, "WebAid/register.html")

def opportunities(request):
    page = request.GET.get('page', None)
    filters = {
        'categories': request.GET.get('categories', None),
        'location': request.GET.get('location', None),
        'creation_time': request.GET.get('creation_time', None)
    }
    category = request.GET.get('category', None)

    if page:
        opportunities = Opportunity.get_latest()

        # Filter opportunities
        if filters['categories']:
            categories = filters['categories'].split(',')
            f = makeCategoryFilter(categories)
            opportunities = list(filter(f, opportunities))
        if filters['location']:
            f = makeLocationFilter(filters['location'])
            opportunities = list(filter(f, opportunities))
        if filters['creation_time']:
            f = makeDateFilter(filters['creation_time'])
            opportunities = list(filter(f, opportunities))

        opportunity_paginator = Paginator(opportunities, 10)

        try:
            page_opp = opportunity_paginator.page(page)
        except EmptyPage:
            return JsonResponse({'error': 'This page does not exist'}, status=404)

        result = []
        for opportunity in page_opp.object_list:
            result.append({
                "id": opportunity.id,
                "title": opportunity.title,
                "description": opportunity.description,
                "creation_time": opportunity.creation_time,
                "location": opportunity.location,
                "creator": {
                    "name": opportunity.creator.username,
                    "id": opportunity.creator.id
                }
            })
        return JsonResponse({'opportunities': result, 'pages': opportunity_paginator.num_pages}) # Returns array of opportunities

    if category:
        return render(request, 'WebAid/opportunities.html', {
            'opportunity_count': Opportunity.objects.all().filter(resolved=None).count(),
            'category': category
        })

    return render(request, 'WebAid/opportunities.html', {
        'opportunity_count': Opportunity.objects.all().filter(resolved=None).count()
    })

@login_required
def create(request):
    if request.method == 'POST':
        form = NewOpportunityForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title'].title()
            description = form.cleaned_data['description']
            location = form.cleaned_data['location'].title()
            categories = form.cleaned_data['categories']

            opportunity = Opportunity(title=title, description=description, location=location, categories=categories, creator=request.user)
            opportunity.save()
            return HttpResponseRedirect(reverse('opportunities'))

        else:
            return render(request, 'WebAid/create.html', {
                'form': form
            })
    form = NewOpportunityForm()
    return render(request, 'WebAid/create.html', {
        'form': form
    })

@csrf_exempt
def opportunity(request, opportunity_id):
    try:
        opp = Opportunity.objects.get(pk=opportunity_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('opportunities'))

    if request.method == 'PUT':
        data = json.loads(request.body)
        title = data.get('title', None)
        location = data.get('location', None)
        categories = data.get('categories', None)
        description = data.get('description', None)

        if title:
            opp.title = title.title()
        if location:
            opp.location = location.title()
        if categories:
            if categories.endswith(', '):
                categories = categories[:-len(', ')]
            opp.categories = categories
        if description:
            opp.description = description
        opp.save()
        return HttpResponse('Opportunity saved', status=200)

    if request.method == 'POST':
        form = ResolveOpportunityForm(request.POST)
        if form.is_valid():
            resolvers_raw = form.cleaned_data['resolvers'].split(',')
            summary = form.cleaned_data['summary']

            resolvers = []
            for resolver in resolvers_raw:
                if resolver.strip() == request.user.username:
                    continue
                try:
                    resolvers.append(User.objects.get(username=resolver.strip()))
                except ObjectDoesNotExist:
                    form.add_error('resolvers', f'User {resolver.strip()} does not exist')
                    return render(request, 'WebAid/opportunity.html', {
                        'opportunity': opp,
                        'form': NewConversationForm({'subject': f'Volunteering for {opp.title}', 'users': opp.creator.username}),
                        'resolve_form': form,
                        'show_resolve': True
                    })

            resolve = Resolve(summary=summary)
            resolve.save()
            resolve.resolvers.set(resolvers)
            opp.resolved = resolve
            opp.save()

    opp.creation_time = opp.creation_time.strftime("%d/%m/%Y")
    categories = []
    for category in opp.categories.split(','):
        categories.append(category.strip())
        opp.categories = categories

    return render(request, 'WebAid/opportunity.html', {
        'opportunity': opp,
        'form': NewConversationForm({'subject': f'Volunteering for {opp.title}', 'users': opp.creator.username}),
        'resolve_form': ResolveOpportunityForm()
    })

@csrf_exempt
def user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'PUT':
        data = json.loads(request.body)
        location = data.get('location', None)
        skills = data.get('skills', None)

        if location:
            user.location = location.title()
        if skills:
            if skills.endswith(', '):
                skills = skills[:-len(', ')]
            user.skills = skills
        user.save()
        return HttpResponse('User saved', status=200)

    user.date_joined = user.date_joined.strftime("%d/%m/%Y")
    user.last_login = user.last_login.strftime("%d/%m/%Y")
    skills = []
    for skill in user.skills.split(','):
        skills.append(skill.strip())
    user.skills = skills

    return render(request, 'WebAid/user.html', {
        'user': user,
        'form': NewConversationForm({'users': user.username})
    })

@csrf_exempt
def messaging(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        text = data.get('text', None)
        conversation = data.get('conversation', None)

        if not text or not conversation:
            return HttpResponse('Pass text and conversation id in request body', status=400)

        conversation =  Conversation.objects.get(pk=conversation)
        message = Message(body=text, sender=request.user, conversation=conversation)
        message.save()

        return HttpResponse('Message saved', status=200)

    if request.method == 'POST':
        form = NewConversationForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            users = form.cleaned_data['users'].split(',')

            user_objects = []
            for user in users:
                try:
                    user = User.objects.get(username=user.strip())
                except ObjectDoesNotExist:
                    form.add_error('users', f'User {user} does not exist')
                    return render(request, 'WebAid/messaging.html', {
                        'form': form,
                        'go_to': 0
                    })
                if not user == request.user:
                    user_objects.append(user)

            if user_objects == []:
                form.add_error('users', 'Must specify at least one other user')
                return render(request, 'WebAid/messaging.html', {
                    'form': form,
                    'go_to': 0
                })

            user_objects.append(request.user)

            conversation = Conversation(subject=subject)
            conversation.save()
            conversation.users.set(user_objects)

            return render(request, 'WebAid/messaging.html', {
                'form': NewConversationForm(),
                'go_to': conversation.id
            })

        else:
            return render(request, 'WebAid/messaging.html', {
                'form': form,
                'go_to': 0
            })

    conversations = request.user.conversations.all().order_by('-id')
    action = request.GET.get('action', None)

    if action == 'get_conversations':
        convo_dict = []
        for conversation in conversations:
            convo_dict.append({
                'subject': conversation.subject,
                'id': conversation.id
            })
        return JsonResponse({'conversations': convo_dict}, status=200)

    if action == 'get_messages':
        conversation = request.GET.get('conversation', None)

        if not conversation:
            return JsonResponse({'error': 'specify conversation id'}, status=400)

        try:
            conversation =  request.user.conversations.get(pk=conversation)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'No conversation with id {conversation}'}, status=400)

        messages = []
        for message in conversation.messages.all():
            if message.sender:
                messages.append({
                    'body': message.body,
                    'sender': {
                        'username': message.sender.username,
                        'id': message.sender.id,
                    },
                    'datetime': message.datetime.ctime() if message.datetime.date() < datetime.datetime.now().date() else message.datetime.time().isoformat(timespec='minutes')
                })
            else:
                messages.append({
                    'body': message.body,
                    'sender': {
                        'username': '#',
                        'id': None,
                    },
                    'datetime': message.datetime.ctime() if message.datetime.date() < datetime.datetime.now().date() else message.datetime.time().isoformat(timespec='minutes')
                })

        recipients = []
        for user in conversation.users.all():
            if not user == request.user:
                recipients.append({'username': user.username, 'id': user.id})
        recipients.append({'username': 'You', 'id': None})

        return JsonResponse({'subject': conversation.subject, 'recipients': recipients, 'messages': messages}, status=200)

    if action == 'go_to':
        conversation = request.GET.get('conversation', None)
        return render(request, 'WebAid/messaging.html', {
            'form': NewConversationForm(),
            'go_to': conversation
        })

    if action == 'leave':
        conversation = request.GET.get('conversation', None)
        if not conversation:
            return HttpResponse('Specifiy conversation id', status=400)

        try:
            conversation = Conversation.objects.get(pk=conversation)
        except ObjectDoesNotExist:
            return HttpResponse(f'No conversation with id {conversation}', status=400)

        message = Message(body=f'{request.user} has left this conversation', conversation=conversation)
        message.save()
        conversation.users.remove(request.user)
        if conversation.users.count() < 2:
            conversation.delete()
            return HttpResponse('Conversation deleted', status=200)
        return HttpResponse('User removed from conversation', status=200)

    return render(request, 'WebAid/messaging.html', {
        'form': NewConversationForm()
    })

def search(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('index'))
    query = request.POST.get('search', None)

    users = User.objects.all()
    if request.user.is_authenticated:
        users = users.exclude(pk=request.user.id)

    for user in users:
        if not re.search(query.lower(), user.username.lower())      \
        and not re.search(query.lower(), user.location.lower()):
            users = users.exclude(pk=user.id)

    opportunities = Opportunity.objects.all()

    for opp in opportunities:
        if not re.search(query.lower(), opp.title.lower())          \
        and not re.search(query.lower(), opp.description.lower())   \
        and not re.search(query.lower(), opp.location.lower()):
            opportunities = opportunities.exclude(pk=opp.id)

    return render(request, 'WebAid/search.html', {
        'users': users,
        'opportunities': opportunities
    })

def helpers(request):
    page = request.GET.get('page', None)
    if page:
        helpers = User.objects.all().annotate(res_count=models.Count('resolved')).exclude(res_count=0).order_by('-res_count')
        helper_paginator = Paginator(helpers, 10)

        try:
            helper_page = helper_paginator.page(page)
        except EmptyPage:
            return JsonResponse({'error': 'This page does not exist'}, status=404)

        result = []
        for helper in helper_page.object_list:
            result.append({
                "id": helper.id,
                "username": helper.username,
                "last_seen": helper.last_login.date(),
                "location": helper.location,
                "helped": helper.resolved.count()
            })
        return JsonResponse({'helpers': result, 'pages': helper_paginator.num_pages}) # Returns array of opportunities
    return render(request, 'WebAid/helpers.html')
