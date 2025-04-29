# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

# Custom User model (optional; can use default User if no extra fields needed)
class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Module(models.Model):
    module_code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.module_code} - {self.name}"

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"

class Professor(models.Model):
    professor_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.professor_id} - {self.name}"

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professors"

class ModuleInstance(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="instances")
    year = models.PositiveIntegerField()
    semester = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])
    professors = models.ManyToManyField(Professor, related_name="module_instances")

    def __str__(self):
        return f"{self.module.module_code} ({self.year}, Sem {self.semester})"

    class Meta:
        verbose_name = "Module Instance"
        verbose_name_plural = "Module Instances"
        unique_together = ['module', 'year', 'semester']

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name="ratings")
    module_instance = models.ForeignKey(ModuleInstance, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.user.username} rated {self.professor.professor_id} in {self.module_instance} as {self.rating}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = ['user', 'professor', 'module_instance']