import jwt
from datetime import datetime, timezone, timedelta
from utils.exceptions import TokenInvalidException
import consts


class _TokenProvider:
    
    def __init__(self) -> None:

        # Get the secrets
        self._access_secret = consts.ENV.get("ACCESS_SECRET")
        self._refresh_secret = consts.ENV.get("REFRESH_SECRET")
        
        # Create required timedeltas
        self._access_token_timedelta = timedelta(minutes= consts.ACCESS_TOKEN_VALID_MINUTES)
        self._refresh_token_timedelta = timedelta(days= consts.REFRESH_TOKEN_VALID_DAYS)

        # Check if secrets are configured
        if None in [self._access_secret, self._refresh_secret]:
            raise AttributeError("ACCCESS_SECRET and REFRESH_SECRET must be configured in .env")
        

    def create_refresh_token(self, user_id: str) -> str:
        """ Creates a refresh token

        Args:
            user_id (str): user's unique id

        Returns:
            str: a refresh token
        """
        payload = {
            "user_id": user_id,
            "exp": datetime.now(tz=timezone.utc) + self._refresh_token_timedelta
        }

        return jwt.encode(
            payload= payload,
            key = self._refresh_secret,
            algorithm = consts.JWT_SIGNING_ALGORITHM
        )
    
    
    def decode_refresh_token(self, token: str) -> dict:
        """ Decodes a given refresh token

        Args:
            token (str): a refresh token

        Raises:
            TokenInvalidException: if jwt is invalid

        Returns:
            dict: a decoded data
        """
        try:
            refresh_decoded = jwt.decode(
                jwt = token,
                key =self._refresh_secret,
                algorithms= [consts.JWT_SIGNING_ALGORITHM]
            )

            return refresh_decoded
        
        except jwt.InvalidTokenError:
            raise TokenInvalidException("Invalid refresh token")
        

    def create_access_token(self, refresh_token: str) -> str:
        """Check the refresh token and create an access token

        Args:
            refresh_token (str): a refresh token

        Raises:
            TokenInvalidException: if the refresh token is invalid

        Returns:
            str: an access token
        """

        try:
            refresh_decoded = self.decode_refresh_token(refresh_token)

        except TokenInvalidException:
            raise TokenInvalidException("Invalid refresh token")
        
        user_id = refresh_decoded["user_id"]


        payload = {
            "user_id": user_id,
            "exp": datetime.now(tz=timezone.utc) + self._access_token_timedelta
        }

        return jwt.encode(
            payload= payload,
            key = self._access_secret,
            algorithm = consts.JWT_SIGNING_ALGORITHM
        )
    
    
    def decode_access_token(self, token: str) -> dict:
        """ Decodes a given access token

        Args:
            token (str): access token

        Raises:
            TokenInvalidException: if jwt is invalid

        Returns:
            dict: a decoded data
        """
        try:
            access_decoded = jwt.decode(
                jwt = token,
                key =self._access_secret,
                algorithms= [consts.JWT_SIGNING_ALGORITHM]
            )

            return access_decoded
        
        except jwt.InvalidTokenError:
            raise TokenInvalidException("Invalid access token")
        

        