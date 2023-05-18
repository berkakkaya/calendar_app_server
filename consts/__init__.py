from dotenv import dotenv_values


ENV = dotenv_values(".env")

# JWT Configuration
JWT_SIGNING_ALGORITHM = "HS256"

REFRESH_TOKEN_VALID_DAYS = 30
ACCESS_TOKEN_VALID_MINUTES = 10
