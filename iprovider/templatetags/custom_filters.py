from django import template
register = template.Library()

@register.filter
def get_location_display(place):
    """Получить отображаемое название локации"""
    if not place:
        return "Location not specified"

    if place.name:
        return place.name
    elif place.address:
        return place.address
    else:
        location_parts = []
        if place.city and place.city.name:
            location_parts.append(place.city.name)
        if place.country and place.country.name:
            location_parts.append(place.country.name)

        if location_parts:
            return ", ".join(location_parts)
        else:
            return "Location not specified"


@register.filter
def get_full_location(place):
    """Получить полную информацию о локации"""
    if not place:
        return "Location not specified"

    parts = []
    if place.name:
        parts.append(place.name)
    if place.address:
        parts.append(place.address)
    if place.city and place.city.name:
        parts.append(f"City: {place.city.name}")
    if place.country and place.country.name:
        parts.append(f"Country: {place.country.name}")
    return " | ".join(parts) if parts else "Location not specified"