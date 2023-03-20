import mesa
import logging
from pvlib.location import Location
from pvlib.pvsystem import (
    PVSystem,
    sapm_effective_irradiance,
    pvwatts_dc,
    Array,
    FixedMount,
    retrieve_sam,
)
from pvlib.solarposition import get_solarposition
from pvlib.atmosphere import alt2pres, get_relative_airmass, get_absolute_airmass
from pvlib.irradiance import get_total_irradiance, get_extra_radiation, aoi
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS, sapm_cell, sapm_module
from pvlib.modelchain import ModelChain

import pandas as pd


class PVInstallation(mesa.Agent):
    sandia_modules = retrieve_sam("SandiaMod")
    cec_inverters = retrieve_sam("cecinverter")

    def __init__(
        self,
        unique_id: int,
        model: mesa.Model,
        voivodeship: str,
        powiat: str,
        power: float,
        latitude: float,
        longitude: float,
        altitude: float = 0.0,
        timezone: str = "Europe/Warsaw",
    ):
        super().__init__(unique_id, model)
        self.logger = logging.getLogger(__name__)

        self.voivodeship = voivodeship
        self.powiat = powiat
        self.power = power
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)
        self.timezone = timezone

        module = self.sandia_modules["Canadian_Solar_CS5P_220M___2009_"]
        inverter = self.cec_inverters["ABB__MICRO_0_25_I_OUTD_US_208__208V_"]

        temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"][
            "open_rack_glass_glass"
        ]

        mount = FixedMount(surface_tilt=self.latitude, surface_azimuth=180)

        pv_arrays = [
            Array(
                mount=mount,
                module_parameters=module,
                temperature_model_parameters=temperature_model_parameters,
            ),
        ]

        self.location = Location(
            self.latitude, self.longitude, self.timezone, self.altitude
        )

        self.system = PVSystem(arrays=pv_arrays, inverter_parameters=inverter)

        self.model_chain = ModelChain(self.system, self.location)

    def step(self):
        weather = self.model.get_weather_pv(self.latitude, self.longitude)

        self.logger.debug(f"Calculations for PVInstallation id: {self.unique_id}")

        self.model_chain.run_model(weather)

        print(self.model_chain.results.effective_irradiance)
