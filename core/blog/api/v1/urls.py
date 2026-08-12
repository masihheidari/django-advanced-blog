from django.urls import path, include

from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api-view-v1'

router = DefaultRouter()
router.register('post', views.PostModelViewSet, basename='post')
router.register('category', views.CategoryModelViewSet, basename='category')

urlpatterns = router.urls



# urlpatterns = [
    
#     #path('post/<int:id>/', views.postdetail, name='post-detail'),
#     # path('post/', views.postlist, name='post-list'),
#     # path('post/', views.PostList.as_view(), name='post-list'),
#     # path('post/<int:pk>/', views.PostDetail.as_view(), name='post-detail'),
#     path('post/', views.PostViewSet.as_view({'get':'list'}), name='post-list'),
#     path('post/<int:pk>/', views.PostViewSet.as_view({'get':'retrieve'}), name='post-detail'),
# ]
