# Necessary functions and classes:
from __future__ import print_function

# Necessary modules:
import sys
import grpc
import report_pb2
import report_pb2_grpc

# Data for translation:
alignment_list = ["Ally", "Enemy"]
class_list = ["Corvette", "Frigate", "Cruiser", "Destroyer", "Carrier", "Dreadnought"]


# Functions for deserialization:
def bytes_to_alignment(alignment):
    return alignment_list[alignment]


def bytes_to_class(class_):
    return class_list[class_]


# Main process function:
def run():
    args = sys.argv[1:]
   
    with grpc.insecure_channel("localhost:55555") as channel:
        stub = report_pb2_grpc.ReportingServiceStub(channel)

        try:
            coordinates = []
            for arg in args:                
                # Replace non-standard minus signs with standard minus sign
                arg = str(arg.replace('\u2009', ' ').replace('\u2212', '-').replace('\u2013', '-').replace('\u2014', '-'))
                
                # Replace comma with dot if comma is used
                arg = arg.replace(',', '.')
                
                # Convert to float
                try:
                    coords = [float(x) for x in arg.split()]
                    coordinates.extend(coords)
                except ValueError as ve:
                    print(f"Error converting '{arg}' to float: {ve}")
                    raise
            
            print(f"All coordinates: {coordinates}")
            
            if len(coordinates) == 2:
                lat, lon = coordinates
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    output(stub.GetShips(report_pb2.Coordinate(values=coordinates)))
                else:
                    print("ERROR! INCORRECT COORDINATES.")

            elif len(coordinates) == 6:
                lat, _, _, lon, _, _ = coordinates
                if -90 <= lat <= 90 and -180 <= lon <= 180:
                    output(stub.GetShips(report_pb2.Coordinate(values=coordinates)))
                else:
                    print("ERROR! INCORRECT COORDINATES.")
            
            else:
                print(f"ERROR! INCORRECT COUNT OF ARGUMENTS. Expected 2 or 6.")
                return

        except ValueError as ve:
            print(f"VALUE ERROR: {ve}")
        except Exception as e:
            print(f"UNEXPECTED ERROR: {e}")

# Output spaceship:
def output(spaceships):
    if spaceships is not None:
        for ship in spaceships:
            print('{\n' + str(ship))  # JSON like serialized data


if __name__ == "__main__":
    run()