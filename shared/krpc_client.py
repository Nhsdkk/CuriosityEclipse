from krpc import connect
from krpc.services.spacecenter import Resource, ReferenceFrame, CelestialBody

from shared.point import Point
from shared.vector import Vector
from shared.singleton import singleton


@singleton
class KRPCClientSingleton:
    """A singleton class for KRPC client"""

    _client = None

    def __init__(self, address: str, port: int = 1000, stream_port: int = 1001) -> None:
        """
        Get KRPC client instance

        :param address: ip address of the server
        :param port: port of the server
        :param stream_port: port for io stream
        :return: KRPC client instance
        """
        self._client = connect(
            name="KSP_client",
            address=address,
            rpc_port=port,
            stream_port=stream_port,
        )

    def get_current_fuel_resource_objects(self) -> list[Resource]:
        """
        Get all fuel objects.

        :return: List of Resource objects, that corresponds to fuel
        """
        resources = self._client.space_center.active_vessel.resources.all
        return [
            resource
            for resource in resources
            if "Fuel" in resource.name or "fuel" in resource.name
        ]

    def get_current_resource_amount_by_name(self, name: str) -> float:
        """
        Get total resource amount by name at the particular moment.

        :param name: Name of the resource
        :return: Total amount of the resource
        """
        return self._client.space_center.active_vessel.resources.amount(name)

    def get_current_total_mass(self) -> float:
        """
        Get total mass of the rocket at the particular moment

        :return: total mass of the rocket
        """
        return self._client.space_center.active_vessel.mass

    def get_current_pos(self, reference: ReferenceFrame = None) -> Point:
        """
        Get current position point

        :param reference: reference object, from which position will be calculated
        :return: position point
        """
        if reference is None:
            reference = self._client.space_center.bodies["Kerbin"].reference_frame

        return Point(*self._client.space_center.active_vessel.position(reference))

    def get_celestial_body_radius(self, celestial_body: CelestialBody = None) -> float:
        """
        Get celestial body radius.

        :param celestial_body: Celestial body, which radius will be calculated.
        :return: Celestial body radius.
        """
        if celestial_body is None:
            celestial_body = self._client.space_center.bodies["Kerbin"]

        pos_point = Point(
            self._client.space_center.active_vessel.position(
                celestial_body.reference_frame
            )
        )
        zero_point = Point()

        return Vector(zero_point, pos_point).modulo

    def get_current_velocity(self, celestial_body: CelestialBody = None) -> float:
        """
        Get current velocity.

        :param celestial_body: Celestial body, from which the velocity will be calculated
        :return:
        """
        if celestial_body is None:
            reference_frame = self._client.space_center.bodies["Kerbin"].reference_frame
        else:
            reference_frame = celestial_body.reference_frame

        point = Point(
            *self._client.space_center.active_vessel.velocity(reference_frame)
        )
        zero_point = Point()

        return Vector(point, zero_point).modulo

    def get_current_pressure(self, celestial_body: CelestialBody) -> float:
        """
        Get current atmosphere pressure at the celestial body.

        :param celestial_body: Celestial body, where the pressure will be calculated
        :return: pressure value
        """
        if celestial_body is None:
            celestial_body = self._client.space_center.bodies["Kerbin"]

        abs_pos = Point(
            self._client.space_center.active_vessel.position(
                celestial_body.reference_frame
            )
        )
        zero_point = Point()
        altitude = Vector(abs_pos, zero_point).modulo

        return celestial_body.pressure_at(altitude)

    def get_celestial_body_by_name(self, celestial_body_name: str) -> CelestialBody:
        """
        Get celestial body by object name.

        :param celestial_body_name: Celestial body name
        :return: Celestial body object
        """
        celestial_body = self._client.space_center.bodies.get(celestial_body_name)
        if celestial_body_name is None:
            raise KeyError(f"Celestial body with name {celestial_body_name}")

        return celestial_body

    def get_current_time(self) -> float:
        """
        Get time elapsed from start.

        :return: time elapsed from start
        """
        return self._client.space_center.active_vessel.met
