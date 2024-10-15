# api/urls.py
from django.urls import path
from .views import RegisterView, LoginView, MatchView, match_result,get_matched_user,CancelMatchView,LikeView,friends_list
from .views import database_monitor,clear_database,online_users,matching_pool,HeartbeatView,CheckOnlineStatusView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('match/', MatchView.as_view(), name='match'),
    path('cancel-match/', CancelMatchView.as_view(), name='cancel-match'),
    path('match-result/<str:username>/', match_result, name='match-result'),
    path('get-matched-user/<int:match_id>/', get_matched_user, name='get-matched-user'),
    
    
    # path('matching_pool/', MatchingPoolView.as_view(), name='matching_pool'),
    # path('online-users/', online_users, name='online_users'),

    path('like/', LikeView.as_view(), name='like'),
    path('friends/', friends_list, name='friends_list'),
    
    
    path('monitor/', database_monitor, name='database_monitor'),
    path('clear-database/', clear_database, name='clear_database'),  # 清空資料庫路由
    path('online-users/', online_users, name='online_users'),
    path('matching-pool/', matching_pool, name='matching_pool'),
    
    path('heartbeat/', HeartbeatView.as_view(), name='heartbeat'),
    path('check-online-status/', CheckOnlineStatusView.as_view(), name='check-online-status'),
]
