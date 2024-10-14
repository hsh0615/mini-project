# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from django.db import IntegrityError
# api/views.py
# 確保導入的是自訂的 User 模型
from .models import User  # 而非 from django.contrib.auth.models import User
#match-view solved (2024/10/14 )
from .models import Match, Like, Friendship

import logging

import redis


# 初始化 Redis 連接
redis_client = redis.Redis(host='localhost', port=6379, db=0)

logger = logging.getLogger(__name__)

# # 配對池和配對結果
# matching_pool = []
# match_results = {}


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"Status": "Success", "Data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {"Status": "Failure", "error": "用戶名已存在"},
                    status=status.HTTP_409_CONFLICT
                )
        return Response(
            {"Status": "Failure", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    def post(self, request):
        # 從請求中獲取帳號和密碼
        username = request.data.get('username')
        password = request.data.get('password')

        # 認證使用者
        user = authenticate(username=username, password=password)

        if user:
            # user.is_online = True  # 設置為在線
            # user.save()
            redis_client.set(f"online_users:{username}", "true")  # 使用 Redis 記錄在線狀態
            
            # 如果認證成功，回傳登入成功訊息
            return Response(
                {'message': '登入成功', 'user': {'username': user.username}},
                status=status.HTTP_200_OK
            )
        else:
            # 如果認證失敗，回傳錯誤訊息
            return Response(
                {'message': '帳號或密碼錯誤'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
class AutoLogoutView(APIView):
    def post(self, request):
        username = request.data.get('username')

        try:
            user = User.objects.get(username=username)
            # 從 Redis 中移除在線狀態和配對池
            redis_client.delete(f"online_users:{username}")  
            redis_client.srem('matching_pool', username)  # 確保從配對池中移除
            return Response({'message': '用戶已離線並退出配對池'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': '用戶不存在'}, status=status.HTTP_404_NOT_FOUND)



class MatchView(APIView):
    def post(self, request):
        username = request.data.get('username')
          
        if not username:
            return Response({'message': '用戶名不能為空'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username.strip())  # 去除多餘空白
        except User.DoesNotExist:
            return Response({'message': '該用戶不存在'}, status=status.HTTP_404_NOT_FOUND)

        # # 檢查使用者是否已經在配對池中
        # if username in matching_pool:
        #     return Response({'message': '您已經在等待配對中，請耐心等待'}, status=status.HTTP_400_BAD_REQUEST)

        # matching_pool.append(username)
        
        if redis_client.sismember('matching_pool', username):
            return Response({'message': '您已在配對池中，請稍等'}, status=status.HTTP_400_BAD_REQUEST)

        redis_client.sadd('matching_pool', username)  # 將使用者加入配對池
        logger.info(f"Current matching pool: {redis_client.smembers('matching_pool')}")

        # # 嘗試找到另一個用戶進行配對
        # if len(matching_pool) >= 2:
        #     for other_username in matching_pool:
        #         if other_username != username:
        #             other_user = User.objects.get(username=other_username)
        #             # 從配對池中移除用戶
        #             matching_pool.remove(username)
        #             matching_pool.remove(other_username)
        #             # 創建 Match 實例
        #             match = Match.objects.create(user1=user, user2=other_user)
        #             # 存儲配對結果
        #             match_results[username] = match.id
        #             match_results[other_username] = match.id
        #             logger.info(f"Match created between {username} and {other_username}")
        #             logger.info(f"Match results: {match_results}")
        #             return Response({'message': f'配對成功！配對對象: {other_username}', 'match_id': match.id}, status=status.HTTP_200_OK)
        if redis_client.scard('matching_pool') >= 2:
            other_username = redis_client.spop('matching_pool').decode()
            if other_username != username:
                redis_client.srem('matching_pool', username)
                other_user = User.objects.get(username=other_username)
                user = User.objects.get(username=username)
                match = Match.objects.create(user1=user, user2=other_user)
                redis_client.set(f"match_result:{username}", other_username)
                redis_client.set(f"match_result:{other_username}", username)
                logger.info(f"Match created between {username} and {other_username}")
                return Response(
                    {'message': f'配對成功！配對對象: {other_username}', 'match_id': match.id},
                    status=status.HTTP_200_OK
                )
        return Response({'message': '等待配對中...'}, status=status.HTTP_200_OK)
    
class CancelMatchView(APIView):
    def post(self, request):
        username = request.data.get('username')

        # 從配對池中移除使用者
        if redis_client.sismember('matching_pool', username):
            redis_client.srem('matching_pool', username)
            return Response({'message': f'{username} 已取消配對'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '使用者不在配對池中'}, status=status.HTTP_400_BAD_REQUEST)


# class MatchingPoolView(APIView):
#     def get(self, request):
#         return Response({'matching_pool': matching_pool}, status=status.HTTP_200_OK)

class MatchingPoolView(APIView):
    def get(self, request):
        pool = [user.decode() for user in redis_client.smembers('matching_pool')]
        return Response({'matching_pool': pool}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def match_result(request, username):
#     match_id = match_results.get(username)
#     if match_id:
#         match = Match.objects.get(id=match_id)
#         # 獲取配對對象的用戶名
#         if match.user1.username == username:
#             matched_username = match.user2.username
#         else:
#             matched_username = match.user1.username
#         return Response({'message': f'配對成功！配對對象: {matched_username}', 'match_id': match.id}, status=status.HTTP_200_OK)
#     else:
#         return Response({'message': '等待配對中...'}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def get_matched_user(request, match_id):
#     username = request.GET.get('username')
#     user = User.objects.get(username=username)
#     try:
#         match = Match.objects.get(id=match_id)
#         if match.user1 == user:
#             matched_user = match.user2.username
#         elif match.user2 == user:
#             matched_user = match.user1.username
#         else:
#             return Response({'message': '無效的配對'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({'matched_username': matched_user}, status=status.HTTP_200_OK)
#     except Match.DoesNotExist:
#         return Response({'message': '配對不存在'}, status=status.HTTP_404_NOT_FOUND)
    
# @api_view(['GET'])
# def online_users(request):
#     online_users = User.objects.filter(is_online=True)
#     usernames = [user.username for user in online_users]
#     return Response({'online_users': usernames}, status=status.HTTP_200_OK)
@api_view(['GET'])
def online_users(request):
    keys = redis_client.keys('online_users:*')
    usernames = [key.decode().split(':')[1] for key in keys]
    return Response({'online_users': usernames}, status=status.HTTP_200_OK)


@api_view(['GET'])
def match_result(request, username):
    matched_user = redis_client.get(f"match_result:{username}")
    if matched_user:
        return Response({'message': f'配對對象: {matched_user.decode()}'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': '尚無配對結果'}, status=status.HTTP_200_OK)