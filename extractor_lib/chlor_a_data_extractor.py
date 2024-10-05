import netCDF4
import numpy as np

def chlor_a_data_extractor(nc_file):
    with netCDF4.Dataset(nc_file, 'r') as dataset:
        chlor_a = dataset.variables['chlor_a'][:]
        lat = dataset.variables['lat'][:]
        lon = dataset.variables['lon'][:]
        palette = dataset.variables['palette'][:]

        chlor_a[chlor_a == -32767.0] = np.nan
        lat[lat == -999.0] = np.nan
        lon[lon == -999.0] = np.nan

        json_data = []
        for i in range(len(lat)):
            for j in range(len(lon)):
                if not (type(np.isnan(chlor_a[i, j])) == np.ma.core.MaskedConstant):
                    json_data.append({
                        "lat": float(lat[i]),
                        "lon": float(lon[j]),
                        "chlor_a": float(chlor_a[i, j])
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
                    "chlorophyll_a": data["chlor_a"]
                }
            }
            for data in json_data
        ]
    }

    return geojson