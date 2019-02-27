from rest_framework import serializers
from events.models import Event, Ticket
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']




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


    class Meta:
        model = Event
        fields = ['id', 'title', 'detail',]


class EventDetailSerializer(serializers.ModelSerializer):
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
