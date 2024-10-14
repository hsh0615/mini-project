# api/urls.py
from django.urls import path
from .views import RegisterView, LoginView, MatchView, match_result,MatchingPoolView,AutoLogoutView,online_users,CancelMatchView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', AutoLogoutView.as_view(), name='auto_logout'),
    
    path('match/', MatchView.as_view(), name='match'),
    path('cancel-match/', CancelMatchView.as_view(), name='cancel-match'),
    path('match-result/<str:username>/', match_result, name='match-result'),
    # path('get-matched-user/<int:match_id>/', get_matched_user, name='get-matched-user'),
    
    
    path('matching_pool/', MatchingPoolView.as_view(), name='matching_pool'),
    path('online-users/', online_users, name='online_users'),
]
