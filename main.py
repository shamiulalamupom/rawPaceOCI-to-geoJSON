import json

from extractor_lib.chlor_a_data_extractor import chlor_a_data_extractor
from extractor_lib.rrs_data_extractor import rrs_data_extractor

netcdf_files = ["data/PACE_OCI.20240914.L3m.DAY.RRS.V2_0.Rrs.0p1deg.NRT.nc", "data/PACE_OCI.20240822.L3m.DAY.CHL.V2_0.chlor_a.0p1deg.NRT.nc"]

json_data = rrs_data_extractor(netcdf_files[0])

with open("output_points.json", "w") as f:
    json.dump(json_data, f)