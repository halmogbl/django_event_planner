from rest_framework import serializers
from events.models import Event, Ticket, Following
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class FollowingSerializer(serializers.ModelSerializer):

    user_follow = UserSerializer()
    user_followed  = UserSerializer()
    class Meta:
        model = Following
        fields = '__all__'



class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        my_username = data.get('username')
        my_password = data.get('password')

        try:
            user_obj = User.objects.get(username=my_username)
        except:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError("Incorrect username/password combination! Noob..")

        return data


class EventListSerializer(serializers.ModelSerializer):

    detail = serializers.HyperlinkedIdentityField(
            view_name = 'api-detail',
            lookup_field = 'id',
            lookup_url_kwarg = 'event_id',
        )

    tickets_count = serializers.SerializerMethodField()


    class Meta:
        model = Event
        fields = ['id', 'title', 'detail','tickets_count']

    def get_tickets_count(self, obj):
        return obj.tickets.count()



class TicketListSerializer(serializers.ModelSerializer):


    user = UserSerializer()

    event = EventListSerializer()

    class Meta:
        model = Ticket
        fields = '__all__'

    def get_booking(self, obj):
        return obj.tickets.count()




class EventDetailSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True)

    added_by = UserSerializer()




    update = serializers.HyperlinkedIdentityField(
            view_name = 'api-update',
            lookup_field = 'id',
            lookup_url_kwarg = 'event_id',
        )
    delete = serializers.HyperlinkedIdentityField(
            view_name = 'api-delete',
            lookup_field = 'id',
            lookup_url_kwarg = 'event_id',
        )

    class Meta:
        model = Event
        fields = '__all__'


class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['added_by',]

class TicketCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        exclude = ['user','event',]