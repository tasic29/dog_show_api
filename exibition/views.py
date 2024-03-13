from django.db.models import Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.viewsets import ModelViewSet
from exibition.pagination import DefaultPagination
from exibition.permissions import DogPermission, IsAdminOrReadOnly, VotePermission


from exibition.serializers import (BreedSerializer,
                                   CreateVoteSerializer,
                                   DogSerializer, GetDogSerializer,
                                   JudgeSerializer,
                                   ShowSerializer,
                                   OwnerSerializer,
                                   SponsorSerializer,
                                   UpdateVoteSerializer,
                                   VoteSerializer)

from .models import Owner, Breed, Dog, Show, Sponsor, Judge, Vote


class OwnerListView(ListAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    pagination_class = DefaultPagination
    search_fields = ['user__first_name', 'user__last_name']
    ordering_fields = ['id']
    permission_classes = [AllowAny]


class OwnerRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['GET', 'PUT'])
    def me(self, request):
        owner = Owner.objects.get(user=request.user)
        if request.method == 'GET':
            serializer = OwnerSerializer(owner)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = OwnerSerializer(owner, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = DefaultPagination
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    permission_classes = [IsAdminOrReadOnly]


class DogViewSet(ModelViewSet):
    queryset = Dog.objects.select_related('owner').annotate(
        votes_count=Count('votes'), total_points=Sum('votes__point')).all()
    serializer_class = DogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['breed']
    pagination_class = DefaultPagination
    search_fields = ['name', 'breed__name']
    ordering_fields = ['id', 'name']
    permission_classes = [DogPermission]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetDogSerializer
        return DogSerializer

    def get_serializer_context(self):
        return {'owner_id': self.request.user.id}


class ShowViewSet(ModelViewSet):
    queryset = Show.objects.all().prefetch_related('sponsor')
    serializer_class = ShowSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sponsor_id']
    pagination_class = DefaultPagination
    search_fields = ['name', 'location']
    ordering_fields = ['id', 'name', 'location']
    permission_classes = [IsAdminOrReadOnly]


class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    permission_classes = [IsAdminOrReadOnly]


class JudgeViewSet(ModelViewSet):
    queryset = Judge.objects.all()
    serializer_class = JudgeSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'first_name', 'last_name']
    permission_classes = [IsAdminOrReadOnly]


class VoteViewSet(ModelViewSet):
    permission_classes = [VotePermission]
    # queryset = Vote.objects.all()

    def get_queryset(self):
        return Vote.objects.filter(dog_id=self.kwargs['dog_pk'])

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateVoteSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return UpdateVoteSerializer
        return VoteSerializer

    def get_serializer_context(self):
        return {
            'dog_id': self.kwargs['dog_pk'],
            'user_id': self.request.user.id
        }
