from krpc import Client, connect


class KRPCClientSingleton:
    """A singleton class for KRPC client"""

    _client = None

    @classmethod
    def create(cls, address: str, port: int = 1000, stream_port: int = 1001) -> Client:
        """
        Get KRPC client instance

        :param address: ip address of the server
        :param port: port of the server
        :param stream_port: port for io stream
        :return: KRPC client instance
        """
        if cls._client is None:
            cls._client = connect(
                name="KSP_client",
                address=address,
                rpc_port=port,
                stream_port=stream_port,
            )
            return cls._client

        return cls._client
