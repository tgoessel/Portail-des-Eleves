from django.contrib.auth import authenticate, get_user_model
from django.utils.six import text_type

from rest_framework import serializers

from authentication.models import User
from authentication.token import Token


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
            "nickname", "birthday", "phone",
            "room", "address", "city_of_origin",
            "option", "is_ast", "is_isupfere", "is_in_gapyear",
            "sports", "roommate", "minesparent"
        )


class TokenSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super(TokenSerializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(
            style={'input_type': 'password'},
            write_only=True
        )

    @classmethod
    def get_token(cls, user):
        return Token.for_user(user)

    def validate(self, attrs):
        self.user = authenticate(**{
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        })
        if self.user is None or not self.user.is_active:
            raise serializers.ValidationError('No active account found with the given credentials')
        data = super(TokenSerializer, self).validate(attrs)

        token = self.get_token(self.user)

        data['access'] = text_type(token)

        return data
