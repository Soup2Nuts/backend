from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from login.models import Account


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirmPassword = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('url', 'username', 'firstName', 'lastName', 'createdAt', 'updatedAt', 'password', 'confirmPassword')
        readOnlyFields = ('createdAt', 'updatedAt')

        def create(self, validatedData):
            return User.objects.create(**validatedData)

        def update(self, instance, validatedData):
            instance.username = validatedData.get('username', instance.username)

            instance.save()

            password = validatedData.get('password', None)
            confirmPassword = validatedData.get('confirmPassword', None)

            if password and confirmPassword and password == confirmPassword:
                instance.setPassword(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance
