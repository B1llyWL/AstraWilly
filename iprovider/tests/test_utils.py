import pytest
from django.utils.translation import  activate
from iprovider.models import Tariff,Category

@pytest.mark.django_db
class TestTranslationMixin:
    """Тесты для миксина TranslationMixin на примере поля description модели Tariff."""

    def test_get_translated_field_fallback_to_default(self):
        """Если перевода нет, возвращается основное поле."""
        category = Category.objects.create(title="Test Cat")
        tariff = Tariff.objects.create(
            title="Original Title",
            price=10.0,
            category=category,
            description="Original Description",
            description_de="",
            description_ru=""
        )
        activate('en')
        assert tariff.get_translated_field('description') == "Original Description"
        activate('de')
        # Немецкий перевод пуст - должен вернуться английский (основной)
        assert  tariff.get_translated_field('description') == "Original Description"

    def test_get_translated_field_with_translation(self):
        """Если перевод есть, возвращается он."""
        category=Category.objects.create(title="Test Cat")
        tariff = Tariff.objects.create(
            title="Original Title",
            price=10.0,
            category=category,
            description = "Original Description",
            description_de = "Deutsche Beschreibung",
            description_ru="Русское описание"
        )
        activate('de')
        assert tariff.get_translated_field('description') == "Deutsche Beschreibung"
        activate('ru')
        assert tariff.get_translated_field('description') == "Русское описание"

    def test_current_language_property(self):
        """Проверка свойства current_language."""
        category = Category.objects.create(title="Test Cat")
        tariff = Tariff.objects.create(
            title="Test",
            price=10.0,
            category=category,
            description="Desc",
            )
        activate('de')
        assert tariff.current_language == 'de'
        # неподдерживаемый язык - должен вернуть 'en'
        activate('fr')
        assert tariff.current_language == 'en'

@pytest.mark.django_db
class TestTariffFeatures:
    """Тесты для метода get_features_list модели Tariff."""
    def test_get_features_list_with_text(self):
        category=Category.objects.create(title="Test Cat")
        tariff = Tariff.objects.create(
            title="Test",
            price=10.0,
            category=category,
            features_text="Feature 1\nFeature 2\n- Feature 3\n• Feature 4"
        )
        expected=["Feature 1", "Feature 2", "Feature 3", "Feature 4"]
        assert tariff.get_features_list() == expected

    def test_get_features_list_empty(self):
        category = Category.objects.create(title="Test Cat")
        tariff = Tariff.objects.create(
            title="Test",
            price=10.0,
            category=category,
            features_text=""
        )
        result = tariff.get_features_list()
        assert isinstance(result, list)
        assert len(result) > 0