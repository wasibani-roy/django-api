from rest_framework import generics, mixins
from django.db.models import Q
from postings.models import BlogPost
from .permissions import IsOwnerOrReadOnly
from .serializers import BlogPostSerializer


class BlogPostAPIView(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk'
    serializer_class        = BlogPostSerializer
    #queryset                = BlogPost.objects.all()

    def get_queryset(self): #used for doing search of data but basic search
        query_set1 = BlogPost.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            query_set1 = query_set1.filter(Q(title__icontains=query)|Q(content__icontains=query)).distinct()
        return query_set1

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field            = 'pk'
    serializer_class        = BlogPostSerializer
    # permission_classes      = [IsOwnerOrReadOnly] #permsission to determine who can access what
    # queryset                = BlogPost.objects.all()

    def get_queryset(self):
        return BlogPost.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

    # def get_object(self):
    #     pk = self.kwargs.get("pk")
    #     return BlogPost.objects.get(pk=pk)
