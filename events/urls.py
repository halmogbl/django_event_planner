
from django.urls import path
from .views import Login, Logout, Signup, home ,dashboard, event_create,event_update, event_list,event_detail

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
	path('event/create/', event_create, name='event-create'),
	path('event/list/', event_list, name='event-list'),
	path('event/detail/<int:event_id>', event_detail, name='event-detail'),
    path('event/update/<int:event_id>', event_update, name='event-update'),




]
