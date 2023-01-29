from gpx_skimap import multi_route_map, load_gpx, plot_euclidean_velocity_route
import pandas as pd

def main():

    GPX_input_Data = ["Sunday2201.gpx",  
                        "Monday2301.gpx",
                        "Tuesday2401.gpx",   
                        "Wednesday2501.gpx",
                        "Thursday2601.gpx",
                        "Friday2701_PM.gpx",
                        "Friday2701_AM.gpx"] 

    local_path = "/Users/ethansimpson/TroisVallees/data"

    input_routes = {route.replace(".gpx",""):load_gpx(f"{local_path}/{route}") for route in GPX_input_Data}

    friday_df = pd.concat([input_routes["Friday2701_AM"],input_routes["Friday2701_PM"]])

    all_routes = {k:v for k,v in input_routes.items() if "Friday" not in k}
    all_routes["Friday2701"] = friday_df

    # For plotting all routes
    _6day_3Valleys_map = multi_route_map(all_routes)
    _6day_3Valleys_map.savemap("6day_3Valleys_map.html")

    # For plotting single velocity map
    day1_speed_map = plot_euclidean_velocity_route(all_routes["Sunday2201"],delta_t=5)
    day1_speed_map.savemap("Day1_SpeedMan.html")

main()