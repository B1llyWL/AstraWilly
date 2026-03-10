import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import  cache
from django.contrib.auth.models import User
from .models import VacancyLocation, Profile, Country, City, Tariff, Separately, Packets

logger = logging.getLogger(__name__)

# Сигналы для обновления стран вакансии при изменении офиса
@receiver(post_save, sender=VacancyLocation)
@receiver(post_delete, sender=VacancyLocation)
def update_vacancy_countries(sender, instance, **kwargs):
    """Обновляет информацию о странах, в которых открыты вакансии, при изменении связанных офисов."""
    instance.vacancy.save()
    logger.debug(f"Vacancy {instance.vacancy.id} countries updated via signal.")

# Сигналы для авто-создания профиля
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает профиль при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"Profile created for user {instance.username}")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
        logger.info(f"Profile auto-created for existing user {instance.username}")

# Сигналы для очистки кэша стран и городов
@receiver(post_save, sender=Country)
@receiver(post_delete, sender=Country)
@receiver(post_save, sender=City)
@receiver(post_delete, sender=City)
def clear_location_cache(sender, **kwargs):
    """Сбрасывает кэш списков стран и городов при их изменении."""
    cache.delete('all_countries')
    cache.delete('all_cities')
    logger.info("Location cache cleared.")

# Сигналы для очистки кэша тарифов и услуг
@receiver(post_save, sender=Tariff)
@receiver(post_delete, sender=Tariff)
@receiver(post_save, sender=Separately)
@receiver(post_delete, sender=Separately)
@receiver(post_save, sender=Packets)
@receiver(post_delete, sender=Packets)
def clear_tariffs_services_cache(sender, **kwargs):
    """Сбрасывает кэш тарифов и услуг при их изменении."""
    cache.delete_pattern('tariffs_data_*')
    cache.delete_pattern('services_data_*')
    logger.info("Tariffs/services cache cleared.")