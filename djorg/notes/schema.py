from graphene_django import DjangoObjectType
import graphene
from .models import PersonalNote as PersonalNoteModel

class PersonalNote(DjangoObjectType):
    
    class Meta:
        model = PersonalNoteModel
        interfaces = (graphene.relay.Node,)
        # Describe the data as a node in the graph

class Query(graphene.ObjectType):
    notes = graphene.List(PersonalNote)

    def resolve_notes(self, info):
        """Decide which notes to return."""
        user = info.context.user #Find with debugger

        if user.is_anonymous:
            return PersonalNoteModel.objects.none()
        elif user.is_superuser:
            return PersonalNoteModel.objects.all()
        else:
            return PersonalNoteModel.objects.filter(user=user)

class CreatePersonalNote(graphene.Mutation):

    class Arguments:
        title = graphene.String()
        content = graphene.String()

    personalnote = graphene.Field(PersonalNote)
    ok = graphene.Boolean()
    status = graphene.String()

    def mutate(self, info, title, content):
        user = info.context.user

        if user.is_anonymous:
            return CreatePersonalNote(ok=False, status="Must be logged in!")
        else:
            newNote = PersonalNote(title=title, content=content, user=user)
            newNote.save()
            return CreatePersonalNote(PersonalNote=newNote, ok=True, status="ok")

class Mutation(graphene.ObjectType):
    create_personal_note = CreatePersonalNote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)