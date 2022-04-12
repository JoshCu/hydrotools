import typing


# local imports
from .type_definitions import LOCATIONS, GeographicScale, GeographicContext, Year


def validate_location(location: str) -> str:
    location_key = LOCATIONS.get(location.lower())  # noqa

    if location_key is None:
        valid_locations = sorted(list(LOCATIONS.keys.union(LOCATIONS.values)))
        error_message = f"Invalid location: {location}. Valid location values are\n{valid_locations}"
        raise ValueError(error_message)

    return location_key


def validate_geographic_scale(geographic_scale: GeographicScale) -> str:
    valid_geo_scales = typing.get_args(GeographicScale)

    if geographic_scale not in valid_geo_scales:
        valid_geo_scales = sorted(valid_geo_scales)
        error_message = f"Invalid geographic scale: {geographic_scale}. Valid geographic scale values are\n{valid_geo_scales}"
        raise ValueError(error_message)

    return geographic_scale


def validate_geographic_context(geographic_context: GeographicContext) -> str:
    valid_geo_contexts = typing.get_args(GeographicContext)

    if geographic_context not in valid_geo_contexts:
        valid_geo_scales = sorted(valid_geo_contexts)
        error_message = f"Invalid geographic context: {geographic_context}. Valid geographic context values are\n{valid_geo_scales}"
        raise ValueError(error_message)

    return geographic_context


def validate_year(year: Year) -> str:
    year_str = str(year)

    valid_years = typing.get_args(Year)
    if year_str not in valid_years:
        valid_years = sorted(valid_years)
        error_message = f"Invalid year: {year}. Valid year values are\n{valid_years}"
        raise ValueError(error_message)

    return year_str
