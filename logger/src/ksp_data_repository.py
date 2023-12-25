from shared.krpc_client import KRPCClient
from shared.singleton import singleton


@singleton
class KspDataRepository(KRPCClient):
    def __init__(self, address: str, port: int, stream_port: int):
        super().__init__(address, port, stream_port)
