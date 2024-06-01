from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from chat.views import imprint_view, index, login_view, logout_view, privacy_policy_view, register_view
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path("chat/", include("chat.urls")),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('imprint/', imprint_view),
    path('privacy_policy/', privacy_policy_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
