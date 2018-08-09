from rest_framework import serializers, viewsets
from .models import PersonalNote

class PersonalNoteSerializer(serializers.HyperlinkedModelSerializer):
    """Describes the model and fields we want to use"""

    def create(self, validated_data):
        # import pdb; pdb.set_trace()
        user = self.context['request'].user
        note = PersonalNote.objects.create(user=user, **validated_data)
        return note

    class Meta:
        model = PersonalNote
        fields = ('title', 'content', 'url')

class PersonalNoteViewSet(viewsets.ModelViewSet):
    """Describes the rows we want from the DB"""

    serializer_class = PersonalNoteSerializer
    queryset = PersonalNote.objects.none()
    # queryset = get_queryset()

    def get_queryset(self):
        # import pdb; pdb.set_trace()
        # pass
        user = self.request.user

        if user.is_anonymous:
            return PersonalNote.objects.none()
        elif user.is_superuser:
            return PersonalNote.objects.all()
        else:
            return PersonalNote.objects.filter(user=user)