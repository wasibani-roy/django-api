from rest_framework import serializers

from postings.models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'pk',
            'id',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        read_only_fields = ['id', 'user', 'pk'] #fields that user cant access

    # converts to JSON
    # validations for data passed
    def validate_title(self, value):
        qs = BlogPost.objects.filter(title__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Title has already been used")
        return value

    # def get_url(self, obj):
    #     # request
    #     request = self.context.get("request")
    #     return obj.get_api_url(request=request)
