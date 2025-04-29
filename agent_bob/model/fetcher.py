import requests

BAXUS_API= "https://services.baxus.co/api/bar/user/"

def get_user_data(username: str) -> dict:
    """
    Fetch user data from the Baxus API.
    
    Args:
        username (str): The username of the user.
        
    Returns:
        json
    """
    url = f"{BAXUS_API}{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
    

    