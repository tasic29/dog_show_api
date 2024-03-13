from django.contrib import admin
from django.db.models import Count

from . models import Owner, Breed, Dog, Judge, Show, Sponsor, Vote

admin.site.register(Judge)
admin.site.register(Vote)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']
    list_select_related = ['user']
    list_per_page = 10


@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'age',
                    'weight', 'color', 'owner_id', 'breed', 'votes_count']
    list_editable = ['weight']
    list_per_page = 10
    search_fields = ['name__istartswith', 'breed__name__istartswith']
    list_filter = ['gender', 'breed']
    autocomplete_fields = ['owner', 'breed']

    def votes_count(self, dog):
        return dog.votes.count()

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(votes_count=Count('votes'))


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {
        'slug': ['name']
    }
    search_fields = ['name__istartswith']


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location',
                    'start_date', 'end_date', 'sponsor']
    list_editable = ['sponsor']
    autocomplete_fields = ['sponsor']
    search_fields = ['name__istartswith', 'location__istartswith']
    list_select_related = ['sponsor']


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'contact_email']
    search_fields = ['sponsor']
