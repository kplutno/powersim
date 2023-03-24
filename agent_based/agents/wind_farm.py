import mesa
from windpowerlib import ModelChain, WindTurbine, create_power_curve
import pandas as pd
from math import sqrt
import matplotlib.pyplot as plt

class WindInstallation(mesa.Agent):
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
    ):
        super().__init__(unique_id, model)
        self.voivodeship = voivodeship
        self.powiat = powiat
        self.power = power
        self.latitude = latitude
        self.longitude = longitude
        self.coordinates = {"P5": P5, "p5": p5}

        turbine = {
            "nominal_power": 3e6,  # in W
            "hub_height": 105,  # in m
            "power_curve": pd.DataFrame(
                data={
                    "value": [
                        p * 1000 for p in [0.0, 26.0, 180.0, 1500.0, 3000.0, 3000.0]
                    ],  # in W
                    "wind_speed": [0.0, 3.0, 5.0, 10.0, 15.0, 25.0],
                }
            ),  # in m/s
        }

        self.turbine = WindTurbine(**turbine)

        self.model_chain_turbine = ModelChain(self.turbine)

    def step(self):
        weather = self.get_wind_weather_data()

        # weather = pd.read_csv(
        #     "./data/sampple_windpowerlib_data.csv",
        #     index_col=0,
        #     header=[0, 1],
        #     date_parser=lambda idx: pd.to_datetime(idx, utc=True),
        # )

        # weather.index = weather.index.tz_convert("Europe/Berlin")

        self.model_chain_turbine.run_model(weather)

        self.turbine.power_output = self.model_chain_turbine.power_output      
        
        self.power = self.turbine.power_output
        
        df = self.power.groupby([self.power.index.day, self.power.index.hour]).sum() * 4
        
        df.plot()

        plt.savefig(f"./data/figures/{self.unique_id}.png")

        plt.close()
        

    def get_wind_weather_data(self):
        weather = self.model.get_weather(self.model.time, self.coordinates)

        weather = weather.drop(["wind_speed", "dni", "dhi", "ghi"], axis=1)

        # Create MultiIndex - windpowerlib uses it
        # Changing name from temp_air to temperature
        variables = [column if column != "temp_air" else "temperature" for column in weather.columns]
        heights = [field.height for field in self.model.config.meteo.fields.values() if field.wind_turbine]
        
        multi_index = [(variable, height) for variable, height in zip(variables, heights)]
        multi_index = pd.MultiIndex.from_tuples(multi_index, names=["variable_name", "height"])
        weather.columns = multi_index
        
        # Calculate value of the wind speed
        for variable, height in weather.columns:
            if "u_" in variable:
                u_name = "u_" + str(int(height))
                v_name = "v_" + str(int(height))
                calculate_speed = lambda row: sqrt(row[u_name]**2 + row[v_name]**2)
                weather[("wind_speed", height)] = weather.apply(calculate_speed , axis=1)

        weather[("roughness_length", 0)] = self.model.config.meteo.wind_constants.roughness
        
        return weather
