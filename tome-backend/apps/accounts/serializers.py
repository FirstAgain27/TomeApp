from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя"""
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(
        write_only=True
    )
    """Указываются только password's, так как эти данные требуют дополнительного внимания, остальные поля
    подтягиваются автоматически"""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'password_confirm', 
            'first_name', 'last_name'
        )
    
    # Метод проверки соответствия паролей, введенных пользователем при регистрации.
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password' : 'Password fields didnt match'}
            )
        return attrs
    
    # Метод создания нового пользователя
    def create(self, validated_data):
        validated_data.pop('password_confirm') 
        """Удаляем потому, что поля нет в БД. Поле виртуальное и существует только в сериализаторе"""

        user = User.objects.create_user(**validated_data)
        return user
    

class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра профиля пользователя"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        fields = (
        'avatar',
        'id', 'username', 'email',          
        'first_name', 'last_name',          
        'full_name',                        
    )
    read_only_fields = ('id', 'created_at', 'updated_at')
    

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя"""
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'avatar', 'bio'
        )

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
   

class UserLoginSerializer(serializers.Serializer):
    # Сериализатор для входа пользователя 
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('Неправильный email или пароль.')
            
            if not user.check_password(password):
                raise serializers.ValidationError('Неправильный email или пароль.')
            
            if not user.is_active:
                raise serializers.ValidationError('Пользователь деактивирован')
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError('Необходимо указать email и пароль.')

class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для смены пароля"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)

    # Проверка старого пароля
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    # Проверка совпадения введенных паролей
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                "Password fields did not match."
            )
        return attrs 
    
    # Сохранение в БД
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user







    