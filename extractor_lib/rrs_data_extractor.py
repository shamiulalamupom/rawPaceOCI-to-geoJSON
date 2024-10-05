import netCDF4
import numpy as np
import json

def rrs_data_extractor(nc_file):
    with netCDF4.Dataset(nc_file, 'r') as dataset:
        Rrs_var = dataset.variables['Rrs']
        Rrs = dataset.variables['Rrs'][:]
        lat = dataset.variables['lat'][:]
        lon = dataset.variables['lon'][:]
        wavelength = dataset.variables['wavelength'][:]

        Rrs[Rrs == -32767.0] = np.nan
        lat[lat == -999.0] = np.nan
        lon[lon == -999.0] = np.nan

        json_data = []
        for lat_point in range(len(lat)):
            for lon_point in range(len(lon)):
                for wavelength_index in range(len(wavelength)):
                    if not (type(np.isnan(Rrs[lat_point, lon_point, wavelength_index])) == np.ma.core.MaskedConstant):
                        json_data.append({
                            "lat": float(lat[lat_point]),
                            "lon": float(lon[lon_point]),
                            "wavelength": int(wavelength[wavelength_index]),
                            "Rrs": float(Rrs[lat_point, lon_point, wavelength_index] * Rrs_var.scale_factor + Rrs_var.add_offset)
                        })

        geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [data["lon"], data["lat"]]
                },
                "properties": {
                    "wavelength": data["wavelength"],
                    "Rrs": data["Rrs"]
                }
            }
            for data in json_data
        ]
    }

    return geojson