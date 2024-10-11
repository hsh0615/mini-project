# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.db import IntegrityError
# api/views.py
from django.contrib.auth.models import User
from .models import Match, Like, Friendship

# 配對池和配對結果
matching_pool = []
match_results = {}

# 註冊視圖
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': '用戶名已存在'}, status=status.HTTP_409_CONFLICT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 登入視圖
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            return Response({'message': '登入成功', 'user': {'username': user.username}}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '帳號或密碼錯誤'}, status=status.HTTP_401_UNAUTHORIZED)

import logging

logger = logging.getLogger(__name__)

class MatchView(APIView):
    def post(self, request):
        username = request.data.get('username')
        
        if not username:
            return Response({'message': '用戶名不能為空'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(username=username)

        if username in matching_pool:
            return Response({'message': '您已經在等待配對中，請耐心等待'}, status=status.HTTP_400_BAD_REQUEST)

        matching_pool.append(username)
        print(f"Current matching pool: {matching_pool}")  # 使用 print() 來輸出配對池
        
        logger.info(f"Current matching pool: {matching_pool}")
        # 嘗試找到另一個用戶進行配對
        if len(matching_pool) >= 2:
            for other_username in matching_pool:
                if other_username != username:
                    other_user = User.objects.get(username=other_username)
                    # 從配對池中移除用戶
                    matching_pool.remove(username)
                    matching_pool.remove(other_username)
                    # 創建 Match 實例
                    match = Match.objects.create(user1=user, user2=other_user)
                    # 存儲配對結果
                    match_results[username] = match.id
                    match_results[other_username] = match.id
                    logger.info(f"Match created between {username} and {other_username}")
                    logger.info(f"Match results: {match_results}")
                    return Response({'message': f'配對成功！配對對象: {other_username}', 'match_id': match.id}, status=status.HTTP_200_OK)

        return Response({'message': '等待配對中...'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def match_result(request, username):
    match_id = match_results.get(username)
    if match_id:
        match = Match.objects.get(id=match_id)
        # 獲取配對對象的用戶名
        if match.user1.username == username:
            matched_username = match.user2.username
        else:
            matched_username = match.user1.username
        return Response({'message': f'配對成功！配對對象: {matched_username}', 'match_id': match.id}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '等待配對中...'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_matched_user(request, match_id):
    username = request.GET.get('username')
    user = User.objects.get(username=username)
    try:
        match = Match.objects.get(id=match_id)
        if match.user1 == user:
            matched_user = match.user2.username
        elif match.user2 == user:
            matched_user = match.user1.username
        else:
            return Response({'message': '無效的配對'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'matched_username': matched_user}, status=status.HTTP_200_OK)
    except Match.DoesNotExist:
        return Response({'message': '配對不存在'}, status=status.HTTP_404_NOT_FOUND)