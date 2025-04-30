import google
from google.auth.transport import Request, requests
from google.oauth2 import id_token


def get_cloud_run_id_token(target_url: str) -> str:
    """Generate ID token for authenticated Cloud Run requests."""
    credentials, _ = google.auth.default()
    auth_req = requests.Request()
    token = id_token.fetch_id_token(auth_req, target_url)
    return token
