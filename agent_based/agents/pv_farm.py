import mesa
import logging
from pvlib.location import Location
from pvlib.pvsystem import (
    PVSystem,
    Array,
    FixedMount,
    retrieve_sam,
)
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS
from pvlib.modelchain import ModelChain
import matplotlib.pyplot as plt
import pandas as pd


class PVInstallation(mesa.Agent):
    modules_database = retrieve_sam("CECMod")
    cec_inverters = retrieve_sam("cecinverter")
    # modules_database.to_csv("./data/CECMod.csv")

    def __init__(
        self,
        unique_id: int,
        model: mesa.Model,
        voivodeship: str,
        powiat: str,
        power: float,
        latitude: float,
        longitude: float,
        P5: str,
        p5: str,
        altitude: float = 0.0,
        timezone: str = "Europe/Warsaw",
    ):
        super().__init__(unique_id, model)
        self.logger = logging.getLogger(__name__)

        self.voivodeship = voivodeship
        self.powiat = powiat

        # Power in Watts (Watt-Peaks)
        self.max_power = power * 1e6
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.altitude = float(altitude)
        self.timezone = timezone
        self.coordinates = {"P5": P5, "p5": p5}
        
        self.power = None
        
        module = self.model.config.pv_panels.Ablytek290
        module_name = module.name
        module_power = module.power_point

        module = self.modules_database[module.name]
        inverter = self.cec_inverters[self.model.config.inverters.ABBMicro.name]

        temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS["sapm"][
            "open_rack_glass_glass"
        ]

        single_module_power = module_power
        number_of_modules = int((self.max_power // single_module_power) + 1)

        mount = FixedMount(surface_tilt=self.latitude, surface_azimuth=180)

        pv_arrays = [
            Array(
                mount=mount,
                module_parameters=module,
                temperature_model_parameters=temperature_model_parameters,
                modules_per_string=number_of_modules,
            ),
        ]

        self.location = Location(
            self.latitude, self.longitude, self.timezone, self.altitude
        )
        self.system = PVSystem(arrays=pv_arrays, inverter_parameters=inverter)
        self.model_chain = ModelChain(
            self.system, self.location, aoi_model="no_loss", spectral_model="no_loss"
        )

        self.results = dict()

    def step(self):
        weather = self.model.get_weather(self.model.time, self.coordinates)

        self.model_chain.run_model(weather)

        self.results[self.model.time] = self.model_chain.results

        self.power = self.model_chain.results.ac

        # Times 4, because freq is 15 minutes, and we want to have Wh
        df = self.power.groupby([self.power.index.day, self.power.index.hour]).sum() * 4
        
        df.plot()

        plt.savefig(f"./data/figures/{self.unique_id}.png")

        plt.close()
