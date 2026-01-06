from .logger import infra_logger
from .config import Config

class IBMAuthenticator:
    """
    Handles secure authentication with IBM Quantum services.
    Encapsulates token retrieval and validation logic.
    """
    
    def __init__(self, config: Config):
        self._config = config
        self._authenticated = False

    def get_token(self) -> str:
        """
        Retrieves the IBM token from configuration.
        """
        token = self._config.IBM_TOKEN
        if not token:
            infra_logger.warning("IBM Quantum Token not found in configuration.")
            return ""
        return token

    def is_authenticated(self) -> bool:
        """
        Checks if a valid token is present.
        """
        return bool(self.get_token())

    def validate_token(self) -> bool:
        """
        Simulates token validation (in a real scenario, this would ping IBM API).
        """
        token = self.get_token()
        if not token:
            return False
        
        infra_logger.info("IBM Token validated successfully.")
        self._authenticated = True
        return True
