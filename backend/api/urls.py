# api/urls.py
from django.urls import path
from .views import RegisterView, LoginView, MatchView, match_result,get_matched_user

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('match/', MatchView.as_view(), name='match'),
    path('match-result/<str:username>/', match_result, name='match-result'),
    path('get-matched-user/<int:match_id>/', get_matched_user, name='get-matched-user'),

]
