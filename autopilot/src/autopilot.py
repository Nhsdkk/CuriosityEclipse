from krpc.services.spacecenter import SASMode

from shared.krpc_client import KRPCClient
from shared.singleton import singleton
import constants


@singleton
class Autopilot(KRPCClient):
    _controller = None

    def __init__(self, address: str, port: int, stream_port: int):
        super().__init__(address, port, stream_port)
        self._controller = self._client.space_center.active_vessel.control

    def _lower_periapsis_altitude(self):
        self._controller.sas = True
        self._controller.sas_mode = SASMode.anti_normal
        current_altitude = self.get_current_altitude()
        self._controller.throttle = 0.1
        while current_altitude > constants.MAX_PERIAPSIS_ALTITUDE:
            pass

        self._controller.throttle = 0
        self._controller.sas_mode = SASMode.normal

    def land(self):
        pass
