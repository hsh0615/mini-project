from rest_framework import serializers
from .models import User  # 引入你自定義的 User 模型

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']  # 根據你的自定義模型調整欄位
        extra_kwargs = {'password': {'write_only': True}}  # 密碼只能寫入，不能讀取

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
