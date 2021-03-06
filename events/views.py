from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, TicketForm
from django.contrib import messages
from .models import Event,Ticket,Following
from django.http import Http404,JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
from hashlib import md5
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    recent_events = Event.objects.filter(date__gte=datetime.today()).order_by('-date','time')[ :10 ]
    
    context = {
        "recent_events": recent_events,
    }
    return render(request, 'home.html',  context)



def event_list(request):   
    events = Event.objects.filter(date__gte=datetime.today()).order_by('-date','time')
    query = request.GET.get('search')
    if query:
        events = events.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(added_by__username__icontains=query)
        ).distinct()

    context = {
       "events": events
    }
    return render(request, 'event_list.html', context)




class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")



class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")



class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")




def event_create(request):
    form = EventForm()
    if request.user.is_anonymous:
        return redirect('login')

    if request.method == "POST":
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.added_by = request.user
            event.save()
            
            # #recive_list= []
            # #followers_emails = request.user.user_followed.all().values_list('user_follow__email',flat=True)
            # for email in followers_emails:
            #     recive_list.append(email)
            
            # #Email to the signed user
            # subject = 'New Event has been created'
            # message = 'new event has created an event'
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = [recive_list]
            # send_mail( subject, message, email_from, recipient_list )


            return redirect('dashboard')
    context = {
        "form":form,
    }
    return render(request, 'event-create.html', context)



def event_update(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.user.is_anonymous:
        return redirect('login')

    if not(request.user.is_staff or request.user == event.added_by):
        raise Http404

    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST,request.FILES ,instance=event)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context = {
        'form': form,
        "event": event,
    }
    return render(request, 'event_update.html', context)



def event_delete(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.user.is_anonymous:
        return redirect('login')
    
    elif not (request.user.is_staff or request.user == event.added_by):
        raise Http404
        
    event.delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('dashboard')



def event_detail(request, event_id):
    if request.user.is_anonymous:
        return redirect('login')
    event = Event.objects.get(id=event_id)
    ticket = TicketForm()

    event_tickets_added = event.tickets.all()
    event_tickets_left = event.seats_left()

    if event_tickets_left <= 0:
        ticket.fields['tickets'].disabled = True

    context = {
        "event": event,
        "ticket": ticket,
        "event_tickets_added": event_tickets_added,
        "event_tickets_left": event_tickets_left
    }
    return render(request, 'event_detail.html', context)



def add_Ticket(request, event_id):
    
    event = Event.objects.get(id=event_id)
    event_tickets_left = event.seats_left()
    ticket_form = TicketForm(request.POST)
    if ticket_form.is_valid():
        booking = ticket_form.save(commit=False)
        if event_tickets_left == 0:
            messages.success(request, "No Seats Availble")
            return redirect('event-detail', event_id )
        elif booking.tickets > event_tickets_left:
            messages.success(request, "Go away integer!")
            return redirect('event-detail', event_id )
        else:
            booking.event = event
            booking.user = request.user
            booking.save()
            subject = 'Django Event Planner'
            #Email to the signed user
            message = 'Thank you for booking from our site'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.user.email]
            send_mail( subject, message, email_from, recipient_list )


            return redirect('dashboard')
    return redirect('event-detail', event_id=event_id)



def dashboard(request):
    if request.user.is_anonymous:
        return redirect('login')
    user_events_added = request.user.events.all()
    user_tickets_added = request.user.tickets.all()
    
    context = {
       "user_events_added":user_events_added,
       "user_tickets_added":user_tickets_added,
    }
    return render(request, 'dashboard.html', context)



def avatar(email, size):
    digest = md5(email.lower().encode('utf-8')).hexdigest()
    return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)



def profile(request):
    if request.user.is_anonymous:
        return redirect('login')
    

    profile_image = avatar(request.user.email, 512)
    profile= request.user
    form = UserSignup(instance=profile)

    user_events = profile.events.all()
    user_followed_obj = User.objects.get(id=request.user.id)

    
    
    # who is following
    my_following = user_followed_obj.user_follow.all()
    my_following_count = user_followed_obj.user_follow.count()
    
    
    
    # who is followers
    followrs = user_followed_obj.user_followed.all()
    follow_count = user_followed_obj.user_followed.count()



    context = {
        "form": form,
        "profile": profile,
        "picture": profile_image,
        "user_events":user_events,
        "follow_count":follow_count,
        "my_following_count":my_following_count,
        "followrs":followrs,
        "my_following": my_following

    }
    return render(request, 'profile.html', context)



def profile_edit(request):
    profile= request.user
    if request.user.is_anonymous:
        return redirect('login')


    form = UserSignup(request.POST, instance=profile)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, "You have successfully updated your profile.")
        login(request, user)
        return redirect("profile")
    return redirect("profile")



def organizer_profile(request,added_by):
    if request.user.is_anonymous:
        return redirect('login')
    
    user = User.objects.get(id=added_by)
    events = Event.objects.filter(added_by = user)
    

    profile_image = avatar(user.email, 512)
    user_followed_obj = User.objects.get(id=added_by)

    #get who's my followre
    follow_count = user_followed_obj.user_followed.count()
    followrs = user.user_followed.all()

    
    #get who I follow
    my_following_count = user_followed_obj.user_follow.count()
    my_following = user_followed_obj.user_follow.all()
    
    if request.user.is_authenticated:
        following = request.user.user_follow.all().values_list('user_followed', flat=True)

    context = {
        "followrs":followrs,
        "my_following":my_following,
        "events": events,
        "user_obj": user,
        "picture": profile_image,
        "following":following,
        "follow_count":follow_count,
        "my_following_count":my_following_count,
    }
    return render(request, 'profile_oranizer.html', context)



def following(request,added_by):
    print("test")
    if request.user.is_anonymous:
        return redirect('signin')
    
        
    user_followed_obj = User.objects.get(id=added_by)
    follow, created = Following.objects.get_or_create(user_follow=request.user, user_followed=user_followed_obj)
    
    if created:
        followed = True
    else:
        followed = False
        follow.delete()

    follow_count = user_followed_obj.user_followed.count()

    #Who many my followre
    my_follow_count = user_followed_obj.user_followed.count()
    #print("my folowres" + str(my_following_count))
   #Who many my Folloing
    my_following_count = user_followed_obj.user_follow.count()
    #print("my following" + my_follow_count))

    response = {
        "followed": followed,
        "follow_count": follow_count,
        "my_following_count":my_following_count
    }
    return JsonResponse(response)
