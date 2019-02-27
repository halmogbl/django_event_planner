
from django.urls import path
from .views import Login, Logout, Signup, home ,dashboard, event_create,event_update, event_list,event_detail, event_delete,add_Ticket, profile_edit, profile, organizer_profile,following
from api.views import (
    EventList,
    EventDetail,
    EventCreate,
    EventUpdate,
    EventDelete,
    UserCreateAPIView,
    UserLoginAPIView,
)

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

	path('event/delete/<int:event_id>', event_delete, name='event-delete'),
	path('ticket/add/<int:event_id>', add_Ticket, name='ticket-create'),
	
	path('profile/edit', profile_edit, name='profile-edit'),
	path('profile/', profile, name='profile'),

	path('organizer/<int:added_by>/', organizer_profile, name='organizer-profile'),
	path('follow/<int:added_by>/', following, name='following'),


	path('api/', EventList.as_view(), name='api-list'),
	path('api/<int:event_id>/', EventDetail.as_view(), name='api-detail'),
	path('api/<int:event_id>/update/', EventUpdate.as_view(), name='api-update'),
	path('api/<int:event_id>/delete/', EventDelete.as_view(), name='api-delete'),
	path('api/add/', EventCreate.as_view(), name='api-create'),
	path('api/signup/', UserCreateAPIView.as_view(), name='api-signup'),
	path('api/signin/', UserLoginAPIView.as_view(), name='api-signin'),

]
