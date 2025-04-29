from rest_framework import serializers
from .models import Module, Professor, ModuleInstance, Rating, User
from django.db.models import Avg

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['professor_id', 'name']

class ModuleInstanceSerializer(serializers.ModelSerializer):
    module_code = serializers.CharField(source='module.module_code')
    module_name = serializers.CharField(source='module.name')
    professors = ProfessorSerializer(many=True)

    class Meta:
        model = ModuleInstance
        fields = ['module_code', 'module_name', 'year', 'semester', 'professors']

class ProfessorRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Professor
        fields = ['professor_id', 'name', 'average_rating']

    def get_average_rating(self, obj):
        avg = obj.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg) if avg is not None else None

class AverageRatingSerializer(serializers.Serializer):
    professor_id = serializers.CharField()
    module_code = serializers.CharField()
    average_rating = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        professor_id = obj['professor_id']
        module_code = obj['module_code']
        avg = Rating.objects.filter(
            professor__professor_id=professor_id,
            module_instance__module__module_code=module_code
        ).aggregate(Avg('rating'))['rating__avg']
        return round(avg) if avg is not None else None

class RatingSerializer(serializers.ModelSerializer):
    professor_id = serializers.CharField(source='professor.professor_id')
    module_code = serializers.CharField(source='module_instance.module.module_code')
    year = serializers.IntegerField(source='module_instance.year')
    semester = serializers.IntegerField(source='module_instance.semester')

    class Meta:
        model = Rating
        fields = ['id', 'user', 'professor_id', 'module_code', 'year', 'semester', 'rating']
        read_only_fields = ['id', 'user']

    def validate(self, data):
        professor_id = data['professor']['professor_id']
        module_code = data['module_instance']['module']['module_code']
        year = data['module_instance']['year']
        semester = data['module_instance']['semester']
        user = self.context['request'].user

        # Check if professor exists
        if not Professor.objects.filter(professor_id=professor_id).exists():
            raise serializers.ValidationError("Professor does not exist.")
        
        # Check if module instance exists
        try:
            module_instance = ModuleInstance.objects.get(
                module__module_code=module_code,
                year=year,
                semester=semester
            )
        except ModuleInstance.DoesNotExist:
            raise serializers.ValidationError("Module instance does not exist.")
        
        # Check if professor teaches this module instance
        if not module_instance.professors.filter(professor_id=professor_id).exists():
            raise serializers.ValidationError("Professor does not teach this module instance.")
        
        # Check for duplicate rating
        if Rating.objects.filter(
            user=user,
            professor__professor_id=professor_id,
            module_instance=module_instance
        ).exists():
            raise serializers.ValidationError("You have already rated this professor in this module instance.")

        return data

    def create(self, validated_data):
        professor_id = validated_data['professor']['professor_id']
        module_code = validated_data['module_instance']['module']['module_code']
        year = validated_data['module_instance']['year']
        semester = validated_data['module_instance']['semester']
        rating_value = validated_data['rating']
        user = self.context['request'].user

        module_instance = ModuleInstance.objects.get(
            module__module_code=module_code,
            year=year,
            semester=semester
        )
        professor = Professor.objects.get(professor_id=professor_id)

        rating = Rating.objects.create(
            user=user,
            professor=professor,
            module_instance=module_instance,
            rating=rating_value
        )
        return rating