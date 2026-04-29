class WaveBenchError(Exception):
    """Base class for expected WaveBench failures."""
    exit_code = 1

class ConfigError(WaveBenchError):
    exit_code = 2

class ConnectionError(WaveBenchError):
    exit_code = 3

class InstrumentError(WaveBenchError):
    exit_code = 4

class OperationTimeout(WaveBenchError):
    exit_code = 5

class DataError(WaveBenchError):
    exit_code = 6
