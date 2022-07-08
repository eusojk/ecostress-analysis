import requests

LOGIN_URL_APPEEARS = "https://appeears.earthdatacloud.nasa.gov/api/login"
USER = ""
PWD = ""


def retrieve_token(user, password):
    """
    :param user:
    :param password:
    :return: json with "token_type", "token", and "expiration" keys OR just {"message": ""} if error occured
    """
    response = requests.post(LOGIN_URL_APPEEARS, auth=(user, password))
    return response.json()
