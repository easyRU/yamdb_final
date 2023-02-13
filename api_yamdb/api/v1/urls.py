from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UsersViewSet,
                    create_user_and_get_email_with_confirmation_code,
                    recieve_token_for_user)

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_patterns = [
    path('token/', recieve_token_for_user, name='recieve_token_for_user'),
    path(
        'signup/',
        create_user_and_get_email_with_confirmation_code,
        name='create_user_and_get_email_with_confirmation_code'
    )
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router_v1.urls)),
]
