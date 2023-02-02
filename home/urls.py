from django.urls import path
from . import views
from home.views import InfoListView, InfoListView2
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.signin),
    path('home', views.home),
    path('lodgingcomplain', views.lodgecomplain),
    path('lodgingforuser', views.lodgingforuser),
    path('reviewlist', views.reviewlist),
    path('review/<str:pk_test>/', views.review, name="review"),
    path('complainlist', views.complainlist),
    path('complain/<str:pk_test>/', views.complain, name="complain"),
    path('registerinfo', views.registerinfo),
    path('signin', views.signin),
    path('signout', views.signout),
    path('lodgecomplain', InfoListView.as_view(), name='main-view'),
    path('lodgeforuser', InfoListView2.as_view()),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
