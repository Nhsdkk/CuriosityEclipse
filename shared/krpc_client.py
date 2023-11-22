from krpc import connect
from krpc.services.spacecenter import Resource, ReferenceFrame, CelestialBody

# from shared.point import Point
# from shared.vector import Vector
from shared.singleton import singleton

KG_IN_TON = 1e3
SOLID_FUEL_UNITS_TO_KG = 7.5
LIQUID_FUEL_UNITS_TO_KG = 5


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

    def get_current_fuel_resource_objects(self) -> list[Resource]:
        """
        Get all fuel objects.

        :return: List of Resource objects, that corresponds to fuel with amount in kg
        """
        resources = self._client.space_center.active_vessel.resources.all
        fuel_resources = [
            resource
            for resource in resources
            if "Fuel" in resource.name or "fuel" in resource.name
        ]

        for fuel_resource in fuel_resources:
            if fuel_resource.name == "SolidFuel":
                fuel_resource.amount *= SOLID_FUEL_UNITS_TO_KG
            else:
                fuel_resource.amount *= LIQUID_FUEL_UNITS_TO_KG

        return fuel_resources

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
