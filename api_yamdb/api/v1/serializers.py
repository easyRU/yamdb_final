from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class TitleReadOnlySerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg',
        read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField()

    def validate(self, value):
        if self.context['request'].method != 'POST':
            return value

        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        title = get_object_or_404(Title, id=title_id)

        if title.reviews.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                f'Отзыв на произведение {title.name} уже существует'
            )
        return value

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'title', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'review', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class UserPatchSerializer(UserSerializer):
    role = serializers.PrimaryKeyRelatedField(read_only=True)


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)

    def validate(self, data):
        email = data['email'].lower()
        username = data['username'].lower()
        if User.objects.filter(username=username, email=email).exists():
            return data
        if username == 'me':
            raise serializers.ValidationError('Нельзя использовать имя "me"!')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                f"Пользователь с username {username} уже зарегистрирован!"
            )
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                f"Пользователь с email {email} уже зарегистрирован!"
            )
        return data


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, allow_blank=False)
    confirmation_code = serializers.CharField(max_length=50, allow_blank=False)
