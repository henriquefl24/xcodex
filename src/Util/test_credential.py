import base64
import requests


def test_credentials(username: str, password: str) -> bool:
    """
    Test if the provided EARTHDATA LOGIN credentials are correct.
    """
    url = "https://urs.earthdata.nasa.gov/api/users/verify_uid"
    auth = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(url, headers=headers)
    return response.status_code == 200
