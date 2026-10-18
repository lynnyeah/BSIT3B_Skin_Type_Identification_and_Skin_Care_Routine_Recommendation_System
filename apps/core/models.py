#from django.db import models

# Create your models here.


from django.conf import settings
from django.db import models


class SkinProfile(models.Model):
    SKIN_TYPES = [
        ("oily", "Oily"),
        ("dry", "Dry"),
        ("normal", "Normal"),
        ("combination", "Combination"),
        ("sensitive", "Sensitive"),
        ("unknown", "Not Yet Identified"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skin_profile",
    )
    skin_type = models.CharField(
        max_length=20,
        choices=SKIN_TYPES,
        default="unknown",
    )
    concerns = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.get_skin_type_display()}"


class SkinAnalysis(models.Model):
    METHODS = [
        ("questionnaire", "Questionnaire"),
        ("camera", "Camera / Photo"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skin_analyses",
    )
    method = models.CharField(max_length=20, choices=METHODS)
    identified_skin_type = models.CharField(
        max_length=20,
        choices=SkinProfile.SKIN_TYPES,
    )
    answers = models.JSONField(default=dict, blank=True)
    image = models.ImageField(
        upload_to="skin_analysis/",
        blank=True,
        null=True,
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.method} - {self.identified_skin_type}"


class SkincareProduct(models.Model):
    CATEGORIES = [
        ("cleanser", "Cleanser"),
        ("toner", "Toner"),
        ("serum", "Serum"),
        ("moisturizer", "Moisturizer"),
        ("sunscreen", "Sunscreen"),
        ("treatment", "Treatment"),
    ]

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    suitable_skin_types = models.JSONField(default=list, blank=True)
    ingredients = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SkincareRoutine(models.Model):
    ROUTINE_TYPES = [
        ("morning", "Morning"),
        ("night", "Night"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="skincare_routines",
    )
    skin_type = models.CharField(
        max_length=20,
        choices=SkinProfile.SKIN_TYPES,
    )
    name = models.CharField(max_length=150)
    routine_type = models.CharField(
        max_length=10,
        choices=ROUTINE_TYPES,
    )
    products = models.ManyToManyField(
        SkincareProduct,
        through="RoutineStep",
        related_name="routines",
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.routine_type}"


class RoutineStep(models.Model):
    routine = models.ForeignKey(
        SkincareRoutine,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    product = models.ForeignKey(
        SkincareProduct,
        on_delete=models.CASCADE,
        related_name="routine_steps",
    )
    step_number = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)

    class Meta:
        ordering = ["step_number"]
        constraints = [
            models.UniqueConstraint(
                fields=["routine", "step_number"],
                name="unique_routine_step_number",
            )
        ]

    def __str__(self):
        return f"{self.routine.name} - Step {self.step_number}"
