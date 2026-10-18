
from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.core.models import (
    SkinProfile,
    SkinAnalysis,
    SkincareProduct,
    SkincareRoutine,
    RoutineStep,
)


class SkincareSystemTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

    def test_create_skin_profile(self):
        profile = SkinProfile.objects.create(
            user=self.user,
            skin_type="oily",
            concerns="Excess oil and shiny skin",
        )

        self.assertEqual(profile.skin_type, "oily")
        self.assertEqual(profile.user, self.user)

    def test_create_skin_analysis(self):
        analysis = SkinAnalysis.objects.create(
            user=self.user,
            method="questionnaire",
            identified_skin_type="combination",
            answers={
                "oily_tzone": True,
                "dry_cheeks": True,
            },
        )

        self.assertEqual(
            analysis.identified_skin_type,
            "combination",
        )
        self.assertEqual(analysis.method, "questionnaire")

    def test_create_skincare_product(self):
        product = SkincareProduct.objects.create(
            name="Gentle Facial Cleanser",
            category="cleanser",
            description="A gentle daily facial cleanser.",
            suitable_skin_types=["oily", "combination"],
        )

        self.assertEqual(product.name, "Gentle Facial Cleanser")
        self.assertTrue(product.is_active)

    def test_create_skincare_routine_with_steps(self):
        product = SkincareProduct.objects.create(
            name="Daily Moisturizer",
            category="moisturizer",
            description="A daily moisturizer.",
            suitable_skin_types=["dry", "normal"],
        )

        routine = SkincareRoutine.objects.create(
            user=self.user,
            skin_type="dry",
            name="Dry Skin Morning Routine",
            routine_type="morning",
        )

        step = RoutineStep.objects.create(
            routine=routine,
            product=product,
            step_number=1,
            instructions="Apply gently to the face.",
        )

        self.assertEqual(routine.steps.count(), 1)
        self.assertEqual(step.product, product)
        self.assertEqual(routine.products.count(), 1)
