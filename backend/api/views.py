# api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.db import IntegrityError
# api/views.py
# 確保導入的是自訂的 User 模型
from .models import User  # 而非 from django.contrib.auth.models import User
#match-view solved (2024/10/14 )
from .models import Match, Like, Friendship

import logging

import redis

from django.db.models import Q

# 初始化 Redis 連接
redis_client = redis.Redis(host='localhost', port=6379, db=0)

logger = logging.getLogger(__name__)

# # 配對池和配對結果
# matching_pool = []
# match_results = {}

from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse


# 定義要操作的表格
TARGET_TABLES = ['api_user', 'api_match', 'api_friendship', 'api_like', 'api_message']

def database_monitor(request):
    table_data = []

    with connection.cursor() as cursor:
        for table in TARGET_TABLES:
            # 取得資料表的記錄數量
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]

            # 取得欄位名稱，確保欄位順序正確
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}' ORDER BY ordinal_position;")
            columns = [col[0] for col in cursor.fetchall()]

            # 查詢所有資料
            cursor.execute(f"SELECT * FROM {table};")
            records = cursor.fetchall()

            # 儲存資料表資訊
            table_data.append({
                'name': table,
                'count': count,
                'columns': columns,
                'records': records
            })

    return render(request, 'monitor.html', {'tables': table_data})

@csrf_exempt
def clear_database(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            for table in TARGET_TABLES:
                cursor.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
        return JsonResponse({'message': '資料庫已清空！'}, status=200)
    return JsonResponse({'message': '無效的請求方式'}, status=405)

@api_view(['GET'])
def online_users(request):
    keys = redis_client.keys('online_users:*')
    usernames_with_ttl = []
    
    for key in keys:
        username = key.decode().split(':')[1]
        ttl = redis_client.ttl(key)  # 獲取剩餘 TTL
        usernames_with_ttl.append({'username': username, 'ttl': ttl})

    return Response({'online_users': usernames_with_ttl}, status=status.HTTP_200_OK)

def matching_pool(request):
    pool = [user.decode() for user in redis_client.smembers('matching_pool')]
    return JsonResponse({'matching_pool': pool})



#----註冊登入---
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(
                    {
                        "data": {
                            "id": user.id,
                            "username": user.username
                        },
                        "message": "註冊成功"
                    },
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {
                        "error": {
                            "code": "USER_ALREADY_EXISTS",
                            "message": "用戶名已存在"
                        }
                    },
                    status=status.HTTP_409_CONFLICT
                )
        return Response(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "輸入格式有誤",
                    "details": serializer.errors
                }
            },
            status=status.HTTP_400_BAD_REQUEST
        )



# 初始化 Redis 連接
redis_client = redis.Redis(host='localhost', port=6379, db=0)
#---使用者登入後快取到redis，並設定60秒過期---
class LoginView(APIView):
    def post(self, request):
        # 從請求中獲取帳號和密碼
        username = request.data.get('username')
        password = request.data.get('password')

        # 優先檢查 Redis 是否有用戶快取資料
        cached_user = redis_client.get(f"user_cache:{username}")

        if cached_user:
            # 如果快取存在，解析資料並返回登入成功
            user_data = eval(cached_user.decode('utf-8'))  # 將字串轉回字典
            print(f"從 Redis 快取取得使用者資料: {user_data}")
            return Response(
                {"data": user_data, "message": "登入成功（快取）"},
                status=status.HTTP_200_OK
            )
            
        # 認證使用者
        user = authenticate(username=username, password=password)

        if user:
            try:
                # # 使用 Redis 記錄在線狀態
                # redis_client.set(f"online_users:{username}", "true")

                # 如果驗證成功，將用戶資料存入 Redis，TTL 設為 60 秒
                user_data = {"id": user.id, "username": user.username}
                redis_client.set(f"user_cache:{username}", str(user_data), ex=60)

                print(f"已快取使用者資料: {user_data}")
                # 如果認證成功，回傳登入成功訊息
                
                return Response(
                    {
                        "message": "登入成功",
                        "data": {
                            "username": user.username
                        }
                    },
                    status=status.HTTP_200_OK
                )
            except redis.RedisError as e:
                # 如果 Redis 連接出現問題，回傳錯誤訊息
                return Response(
                    {
                        "error": {
                            "code": "REDIS_ERROR",
                            "message": "無法記錄在線狀態，請稍後再試"
                        }
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # 如果認證失敗，回傳錯誤訊息
            return Response(
                {
                    "error": {
                        "code": "INVALID_CREDENTIALS",
                        "message": "帳號或密碼錯誤"
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

class HeartbeatView(APIView):
    def post(self, request):
        username = request.data.get('username')

        # 更新使用者的在線狀態，TTL 設為 60 秒
        redis_client.set(f"online_users:{username}", "true", ex=60)

        return Response({"message": "在線狀態已更新"}, status=200)

class CheckOnlineStatusView(APIView):
    def get(self, request, username):
        # 檢查 Redis 是否有該使用者的在線狀態
        is_online = redis_client.exists(f"online_users:{username}")

        if is_online:
            return Response({"username": username, "status": "online"}, status=200)
        else:
            return Response({"username": username, "status": "offline"}, status=200)
            


class MatchView(APIView):
    def post(self, request):
        username = request.data.get('username')
        print("Received username:", username)  # 调试信息

        if not username:
            return Response({'message': '用戶名不能為空'}, status=status.HTTP_400_BAD_REQUEST)

        username = username.strip()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'message': '該用戶不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 检查用户是否在线
        if not redis_client.exists(f"online_users:{username}"):
            return Response({'message': '用戶不在線，不能進行配對'}, status=status.HTTP_400_BAD_REQUEST)

        # 使用 Redis 事务来保证原子性
        with redis_client.pipeline() as pipe:
            while True:
                try:
                    # 监视匹配池
                    pipe.watch('matching_pool')

                    # 检查用户是否已在匹配池中
                    if pipe.sismember('matching_pool', username):
                        pipe.unwatch()
                        return Response({'message': '您已在配對池中，請稍等'}, status=status.HTTP_400_BAD_REQUEST)

                    # 获取当前匹配池中的用户
                    matching_pool = pipe.smembers('matching_pool')
                    matching_pool_decoded = [u.decode() for u in matching_pool]
                    print(f"Matching pool before adding {username}: {matching_pool_decoded}")  # 调试信息

                    # 排除当前用户
                    available_users = [u for u in matching_pool_decoded if u != username]
                    print(f"Available users for {username}: {available_users}")  # 调试信息

                    # 开始事务
                    pipe.multi()

                    # 将当前用户添加到匹配池
                    pipe.sadd('matching_pool', username)

                    if available_users:
                        # 与第一个可用用户进行匹配
                        other_username = available_users[0]
                        other_user = User.objects.get(username=other_username)

                        # 从匹配池中移除双方
                        pipe.srem('matching_pool', username)
                        pipe.srem('matching_pool', other_username)

                        # 执行事务
                        pipe.execute()

                        # 创建匹配记录
                        match = Match.objects.create(user1=user, user2=other_user)

                        # 存储匹配结果
                        redis_client.set(f"match_result:{username}", other_username)
                        redis_client.set(f"match_result:{other_username}", username)

                        print(f"Match created between {username} and {other_username}")  # 调试信息

                        return Response(
                            {'message': f'配對成功！配對對象: {other_username}', 'match_id': match.id},
                            status=status.HTTP_200_OK
                        )
                    else:
                        # 没有可用用户，执行事务仅添加自己到匹配池
                        pipe.execute()
                        return Response({'message': '等待配對中...'}, status=status.HTTP_200_OK)
                except redis.WatchError:
                    # 如果在事务期间匹配池被修改，重试
                    continue
                except Exception as e:
                    pipe.reset()
                    print(f"An error occurred: {e}")
                    return Response({'message': '服務器錯誤，請稍後再試'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CancelMatchView(APIView):
    def post(self, request):
        username = request.data.get('username')

        # 從配對池中移除使用者
        if redis_client.sismember('matching_pool', username):
            redis_client.srem('matching_pool', username)
            return Response({'message': '已取消配對'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '使用者不在配對池中'}, status=status.HTTP_400_BAD_REQUEST)


class LikeView(APIView):

    def post(self, request):
        username = request.data.get('username')
        match_id = request.data.get('match_id')

        try:
            user = User.objects.get(username=username)
            match = Match.objects.get(id=match_id)

            # 檢查用戶是否在該配對中
            if user != match.user1 and user != match.user2:
                return Response({'message': '用戶不在該配對中'}, status=status.HTTP_400_BAD_REQUEST)

            # 檢查是否已經點過喜歡
            if Like.objects.filter(match=match, liker=user).exists():
                return Response({'message': '您已經點過喜歡'}, status=status.HTTP_400_BAD_REQUEST)

            # 保存喜歡記錄
            Like.objects.create(match=match, liker=user)

            # 檢查對方是否也點了喜歡
            other_user = match.user2 if user == match.user1 else match.user1
            if Like.objects.filter(match=match, liker=other_user).exists():
                # 雙方都點了喜歡，建立好友關係
                Friendship.objects.create(user1=user, user2=other_user)
                Friendship.objects.create(user1=other_user, user2=user)

                # 將配對結果存入 Redis
                redis_client.set(f"match_result:{user.username}", other_user.username)
                redis_client.set(f"match_result:{other_user.username}", user.username)

                return Response({'message': '恭喜！雙方都喜歡彼此，已建立好友關係。'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': '已送出喜歡，等待對方確認。'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': '用戶不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Match.DoesNotExist:
            return Response({'message': '配對不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_matched_user(request, match_id):
    username = request.GET.get('username')
    if not username:
        return Response({'message': '用戶名不能為空'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
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
    except User.DoesNotExist:
        return Response({'message': '用戶不存在'}, status=status.HTTP_404_NOT_FOUND) 

@api_view(['GET'])
def match_result(request, username):
    matched_user = redis_client.get(f"match_result:{username}")
    if matched_user:
        matched_user = matched_user.decode()
        try:
            user = User.objects.get(username=username)
            matched_user_obj = User.objects.get(username=matched_user)
            match = Match.objects.filter(
                Q(user1=user, user2=matched_user_obj) | Q(user1=matched_user_obj, user2=user)
            ).first()
            if match:
                return Response({
                    'message': f'配對成功！配對對象: {matched_user}',
                    'matched_username': matched_user,
                    'match_id': match.id
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': '尚無配對結果'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': '用戶不存在'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': '尚無配對結果'}, status=status.HTTP_200_OK)
    
    # api/views.py
@api_view(['GET'])
def friends_list(request):
    username = request.GET.get('username')
    if not username:
        return Response({'message': '用戶名不能為空'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username=username)
        # 獲取所有與該用戶有好友關係的用戶
        friendships = Friendship.objects.filter(user1=user)
        friends = [f.user2.username for f in friendships]
        return Response({'friends': friends}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': '用戶不存在'}, status=status.HTTP_404_NOT_FOUND)
