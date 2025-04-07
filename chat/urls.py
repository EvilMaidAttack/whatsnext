from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views
import pprint

router = routers.DefaultRouter()
router.register("chatrooms", views.ChatRoomViewSet, basename="chatrooms")
router.register("profiles", views.ProfileViewSet, basename="customers")
router.register("exports", views.ChatExportViewSet, basename="exports")

chatrooms_router = routers.NestedDefaultRouter(router, "chatrooms", lookup="chatroom")
chatrooms_router.register("messages", views.MessageViewSet, basename="chatroom-messages")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(chatrooms_router.urls))
    ]
