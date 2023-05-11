import json
from typing import Any
from typing import Dict


def read_json_data(
    ego_vehicle_file: str, vehicle_data_file: str
) -> Dict[str, Dict[str, Any]]:
    with open(ego_vehicle_file, "r") as file_object:
        ego_data = json.load(file_object)

    with open(vehicle_data_file, "r") as file_object:
        vehicle_data = json.load(file_object)

    return {"ego_vehicle": ego_data, "vehicles": vehicle_data}


def read_lane_data(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as file_object:
        lane_data: Dict[str, Any] = json.load(file_object)
    return lane_data


def main():
    ego_vehicle_filepath = "data/ego_data.json"
    vehicle_data_filepath = "data/vehicle_data.json"
    data = read_json_data(ego_vehicle_filepath, vehicle_data_filepath)
    print(data['ego_vehicle']['Lane'][:10])
    print(data['ego_vehicle']['Velocity'][:10])

    file_path = "data/lane_data.json"
    lane_data = read_lane_data(file_path)
    print(lane_data['0']['0']['0'])
    print(lane_data['0']['0']['1'])


if __name__ == "__main__":
    main()
