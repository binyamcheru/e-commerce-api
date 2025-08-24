from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True, validators =[validate_password])   
    password2 = serializers.CharField(write_only=True,required=True) 
    profile_image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ('email','password','password2','first_name','last_name','profile_image')

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match."})
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('password2')
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role='customer',  # default role for registration
            is_active=False,  # optional: require email verification
        )  
        user.set_password(validated_data['password'])
        user.save()
        return user

