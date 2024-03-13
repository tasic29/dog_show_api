from django.urls import path
from rest_framework_nested import routers
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import APIView

from . import views


class MyAPIRoot(APIView):

    def get(self, request, *args, **kwargs):
        return Response({
            "breeds": reverse('breed-list', request=request),
            "dogs": reverse('dog-list', request=request),
            "shows": reverse('show-list', request=request),
            "sponsors": reverse('sponsor-list', request=request),
            "judges": reverse('judge-list', request=request),
            "owners": reverse('owners-list', request=request),
        })


router = routers.DefaultRouter()
router.register('breeds', views.BreedViewSet, basename='breed')
router.register('dogs', views.DogViewSet, basename='dog')
router.register('shows', views.ShowViewSet, basename='show')
router.register('sponsors', views.SponsorViewSet, basename='sponsor')
router.register('judges', views.JudgeViewSet, basename='judge')

dogs_router = routers.NestedDefaultRouter(router, 'dogs', lookup='dog')
dogs_router.register('votes', views.VoteViewSet, basename='dog-votes')

urlpatterns = [
    path('', MyAPIRoot.as_view(), name='api-root'),
    path('owners/', views.OwnerListView.as_view(), name='owners-list'),
    path('owners/<int:pk>/', views.OwnerRetrieveUpdateView.as_view(),
         name='owner-detail'),
]

# Include both router URLs
urlpatterns += router.urls
urlpatterns += dogs_router.urls
