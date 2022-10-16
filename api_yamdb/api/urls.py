from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import GetTokenView, SignUpViewSet, UserViewSet

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'auth/signup', SignUpViewSet, basename='signup')
router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
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


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/', GetTokenView.as_view(), name='token_obtain_pair')
]
