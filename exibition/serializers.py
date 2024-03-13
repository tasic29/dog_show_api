from rest_framework import serializers


from exibition.models import Owner, Breed, Dog, Show, Sponsor, Judge, Vote


class OwnerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Owner
        fields = ['id', 'user_id', 'phone', 'address']


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name', 'description']


class SimpleOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'phone', 'address']


class GetDogSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)
    total_points = serializers.IntegerField(read_only=True)
    owner_id = serializers.IntegerField()

    class Meta:
        model = Dog
        fields = ['id', 'owner_id', 'name', 'gender', 'age', 'weight',
                  'color', 'breed', 'votes_count', 'total_points', 'image']


class DogSerializer(serializers.ModelSerializer):
    votes_count = serializers.IntegerField(read_only=True)
    total_points = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = ['id', 'name', 'gender', 'age', 'weight',
                  'color', 'breed', 'votes_count', 'total_points', 'image']

    def create(self, validated_data):
        owner_id = self.context['owner_id']
        return Dog.objects.create(owner_id=owner_id, **validated_data)


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'contact_person',
                  'contact_email', 'contact_phone']


class ShowSerializer(serializers.ModelSerializer):
    sponsor = serializers.PrimaryKeyRelatedField(
        queryset=Sponsor.objects.all()
    )

    class Meta:
        model = Show
        fields = ['id', 'name', 'location',
                  'start_date', 'end_date', 'sponsor']


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ['id', 'name', 'contact_person',
                  'contact_email', 'contact_phone']


class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Judge
        fields = ['id', 'first_name', 'last_name', 'email', 'phone']


class VoteSerializer(serializers.ModelSerializer):
    dog_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ['id', 'dog_id', 'user_id', 'point']


class CreateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['dog_id', 'point']

    def create(self, validated_data):
        dog_id = self.context['dog_id']
        user_id = self.context['user_id']
        return Vote.objects.create(dog_id=dog_id, user_id=user_id, **validated_data)


class UpdateVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['point']
