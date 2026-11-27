import logging
import random
from dataclasses import dataclass

import httpx
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

import osrm

logger = logging.getLogger(__name__)

@dataclass
class Order:
    order_id: int
    pickup_lat: float
    pickup_lon: float
    delivery_lat: float
    delivery_lon: float

@dataclass
class Driver:
    driver_id: int
    lat: float
    lon: float

@dataclass
class StopPoint:
    order_id: int
    stop_type: bool  # 0 - pickup, 1 - delivery
    cumulative_distance_m: int


def _pad_round_matrix(matrix: list[list[float]]) -> list[list[int]]:
    new_matrix = [[round(cell) for cell in row] + [0] for row in matrix]
    new_matrix.append([0 for _ in range(len(matrix))])
    return new_matrix

def prepare_data_for_solver(coordinates: list[tuple[float, float]]) -> dict | None:
    raw_matrices = osrm.get_osrm_matrices(coordinates)  # http client?
    if not raw_matrices: return None
    duration_matrix, distance_matrix = map(_pad_round_matrix, raw_matrices)
    data = {
        "distance_matrix": distance_matrix,
        "num_vehicles": 0,
        "starts": [],
        "ends": [],
        "pickup_deliveries": [[]],
    }
    return data

def process_data(data: dict):  # -> list[route]
    manager = pywrapcp.RoutingIndexManager(
        len(data["distance_matrix"]),
        data["num_vehicles"],
        data["starts"],
        data["ends"],
    )
    routing = pywrapcp.RoutingModel(manager)