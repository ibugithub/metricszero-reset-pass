from stytch import B2BClient as StytchB2BClient
import os
import logging

logger = logging.getLogger(__name__)

_stytch_client = None

def get_stytch_client():
    """Get Stytch client"""
    global _stytch_client
    if _stytch_client is None:
        _stytch_client = StytchB2BClient(
            project_id=os.getenv("STYTCH_PROJECT_ID"),
            secret=os.getenv("STYTCH_SECRET"),
            environment=os.getenv('ENV', 'test')
        )
    return _stytch_client