from botapp.validators import validate_image
from rest_framework import serializers


class AnswerImageSerializer(serializers.Serializer):
    """Сериализатор для графических ответов."""

    file = serializers.ImageField(write_only=True, validators=[validate_image])
    answer_score = serializers.IntegerField(read_only=True)
