from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm
from django.contrib import messages
from .models import Event,Ticket

def home(request):
    recent_events = Event.objects.all()
    context = {
		"recent_events": recent_events,
	}
    return render(request, 'home.html',  context)



def event_detail(request, event_id):
	if request.user.is_anonymous:
		return redirect('login')
	event = Event.objects.get(id=event_id)
    #ticket = Ticket.objects.filter(event=event)


	context = {
		"event": event,
        #"ticket": ticket
	}
	return render(request, 'event_detail.html', context)








def event_list(request):
    events = Event.objects.all()
    query = request.GET.get('q')
    if query:
        event = event.filter(
            Q(title__icontains=query)|
            Q(description__icontains=query)|
            Q(added_by__username__icontains=query)
        ).distinct()


    context = {
       "events": events

    }
    return render(request, 'events.html', context)


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
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.added_by = request.user
            event.save()
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
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			return redirect("dashboard")
	context = {
		'form': form,
		"event": event,
	}
	return render(request, 'event_update.html', context)










def dashboard(request):
    #events_added = Event.objects.all()
    #events = request.user.event.all().values_list('movie', flat=True)

    user_events_added = []
    user_events_added = request.user.event_set.all()
    events = Event.objects.filter(id__in=user_events_added)

    context = {
       "events": events,
       "user_events_added":user_events_added
    }
    return render(request, 'dashboard.html', context)
