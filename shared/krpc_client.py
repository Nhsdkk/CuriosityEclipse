from krpc import connect
from krpc.services.spacecenter import ReferenceFrame, CelestialBody
from enum import Enum

from shared.singleton import singleton
from shared.vector import Vector
from shared.point import Point

KG_IN_TON = 1e3
SOLID_FUEL_UNITS_TO_KG = 7.5
LIQUID_FUEL_UNITS_TO_KG = 5


class FuelType(Enum):
    SOLID_FUEL = "SolidFuel"
    LIQUID_FUEL = "LiquidFuel"


@singleton
class KRPCClientSingleton:
    """A singleton class for KRPC client"""

    _client = None

    def __init__(self, address: str, port: int = 1000, stream_port: int = 1001) -> None:
        """
        Public constructor

        :param address: Ip address of the server
        :param port: Port of the server
        :param stream_port: Port for io stream
        :return: None
        """
        self._client = connect(
            name="KSP_client",
            address=address,
            rpc_port=port,
            stream_port=stream_port,
        )

    def get_fuel_amount(self, fuel_type: FuelType) -> float:
        """
        Get total mass of fuel with type fuel_type.

        :type fuel_type: Type of the fuel
        :return: List of Resource objects, that corresponds to fuel with amount in kg
        """
        resources = self._client.space_center.active_vessel.resources.all
        fuel_resources = [
            resource for resource in resources if fuel_type.value in resource.name
        ]

        if fuel_type == FuelType.SOLID_FUEL:
            return (
                sum([resource.amount for resource in fuel_resources])
                * SOLID_FUEL_UNITS_TO_KG
            )
        else:
            return (
                sum([resource.amount for resource in fuel_resources])
                * LIQUID_FUEL_UNITS_TO_KG
            )

    def get_current_resource_amount_by_name(self, name: str) -> float:
        """
        Get total resource amount by name at the particular moment.

        :param name: Name of the resource
        :return: Total amount of the resource in ksp units
        """
        return self._client.space_center.active_vessel.resources.amount(name)

    def get_current_total_mass(self) -> float:
        """
        Get total mass of the rocket at the particular moment

        :return: Total mass of the rocket in kg
        """
        return self._client.space_center.active_vessel.mass * KG_IN_TON

    # def get_current_pos(self, reference: ReferenceFrame = None) -> Point:
    #     """
    #     Get current position point
    #
    #     :param reference: Reference object, from which position will be calculated
    #     :return: Position point with parameters in meters
    #     """
    #     if reference is None:
    #         reference = self._client.space_center.bodies["Kerbin"].reference_frame
    #
    #     return Point(*self._client.space_center.active_vessel.position(reference))

    def get_current_altitude(self, reference: ReferenceFrame = None) -> float:
        """
        Get current altitude.

        :param reference: Reference object, from which position will be calculated
        :return: Position point with parameters in meters
        """
        if reference is None:
            reference = self._client.space_center.bodies["Kerbin"].reference_frame

        return (
            self._client.space_center.active_vessel.flight(reference).mean_altitude
            + 7.1
        )

    def get_celestial_body_radius(self, celestial_body: CelestialBody = None) -> float:
        """
        Get celestial body radius.

        :param celestial_body: Celestial body, which radius will be calculated.
        :return: Celestial body radius.
        """
        if celestial_body is None:
            celestial_body = self._client.space_center.bodies["Kerbin"]

        return celestial_body.equatorial_radius

    def get_current_velocity(self, celestial_body: CelestialBody = None) -> float:
        """
        Get current velocity.

        :param celestial_body: Celestial body, from which the velocity will be calculated
        :return: Velocity, relative to the celestial body in m / sec
        """
        if celestial_body is None:
            reference_frame = self._client.space_center.bodies["Kerbin"].reference_frame
        else:
            reference_frame = celestial_body.reference_frame

        return self._client.space_center.active_vessel.flight(reference_frame).speed

    def get_current_pressure(self, celestial_body: CelestialBody = None) -> float:
        """
        Get current atmosphere pressure at the celestial body.

        :param celestial_body: Celestial body, where the pressure will be calculated
        :return: Pressure value at current altitude in pascals
        """
        if celestial_body is None:
            celestial_body = self._client.space_center.bodies["Kerbin"]

        return self._client.space_center.active_vessel.flight(
            celestial_body.reference_frame
        ).static_pressure

    def get_celestial_body_by_name(self, celestial_body_name: str) -> CelestialBody:
        """
        Get celestial body by object name.

        :param celestial_body_name: Celestial body name
        :return: Celestial body object
        """
        celestial_body = self._client.space_center.bodies.get(celestial_body_name)
        if celestial_body is None:
            raise KeyError(f"Celestial body with name {celestial_body_name}")

        return celestial_body

    def get_current_time(self) -> float:
        """
        Get time elapsed from start.

        :return: Time elapsed from start in seconds
        """
        return self._client.space_center.active_vessel.met

    def get_current_position(self, reference_frame: ReferenceFrame = None) -> Vector:
        """
        Get vector to current position from reference frame

        :param reference_frame: Reference object from which current position will be calculated
        :return: Vector to current position
        """
        if reference_frame is None:
            reference_frame = self._client.space_center.bodies.get("Kerbin").reference_frame

        zero_point = Point(0, 0, 0)
        end_point = Point(
            *self._client.space_center.active_vessel.position(reference_frame)
        )

        return Vector(zero_point, end_point)

    def get_current_temperature(self) -> float:
        """
        Get current temperature on Kerbin in Kelvin
        :return: Temperature on Kerbin in Kelvin
        """
        kerbin = self._client.space_center.bodies.get("Kerbin")
        pos = self.get_current_position()
        return kerbin.temperature_at((pos.end.x, pos.end.y, pos.end.z), kerbin.reference_frame)
