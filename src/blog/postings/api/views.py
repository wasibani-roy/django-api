from rest_framework import generics, mixins
from postings.models import BlogPost
from .serializers import BlogPostSerializer


class BlogPostAPIView(generics.CreateAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk'
    serializer_class        = BlogPostSerializer
    #queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return BlogPost.objects.all()


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk'
    serializer_class        = BlogPostSerializer
    # queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return BlogPost.objects.all()

    # def get_serializer_context(self, *args, **kwargs):
    #     return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)
