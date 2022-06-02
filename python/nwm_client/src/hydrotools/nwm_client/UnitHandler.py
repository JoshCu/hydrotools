import pint
from dataclasses import dataclass
import numpy.typing as npt
import pandas as pd

@dataclass
class UnitHandler:
    """Engine to handle unit of measurement conversions.

    Attributes
    ----------
    unit_registry: pint.UnitRegistry, default pint.UnitRegistry(cache_folder=":auto:")
        pint.UnitRegistry that handles all units used by UnitHandler.
    
    """
    unit_registry: pint.UnitRegistry = pint.UnitRegistry(cache_folder=":auto:")

    def conversion_factor(self, from_units: str, to_units: str) -> float:
        """Compute and return a conversion factor from from_units to 
        to_units.
        
        Parameters
        ----------
        from_units: pint.UnitRegistry.Quantity compatible str
            Units from which to convert (e.g. "m^3/s")
        to_units: pint.UnitRegistry.Quantity compatible str
            Desired conversion units (e.g. "ft^3/s")
            
        Returns
        -------
        result: float
            Conversion factor to transform from_units to to_units.

        Example
        -------

        """
        # Return conversion factor
        return self.unit_registry.Quantity(1, from_units).to(to_units).magnitude

    def convert_values(self, value: npt.ArrayLike, from_units: str, to_units: str) -> npt.ArrayLike:
        """Convert value from from_units to to_units.
        
        Parameters
        ----------
        value: array-like, required
            Values to convert.
        from_units: pint.UnitRegistry.Quantity compatible str
            Units from which to convert (e.g. "m^3/s")
        to_units: pint.UnitRegistry.Quantity compatible str
            Desired conversion units (e.g. "ft^3/s")
            
        Returns
        -------
        result: array-like
            Converted values same shape as value.

        Example
        -------

        """
        # Check for pandas.series
        if isinstance(value, pd.Series):
            return pd.Series(
                data=self.unit_registry.Quantity(value.values, from_units).to(to_units).magnitude,
                index=value.index
            )

        # Return converted value
        return self.unit_registry.Quantity(value, from_units).to(to_units).magnitude
