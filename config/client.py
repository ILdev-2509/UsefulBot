from service.API_client import APIClient, RequestsClient
from config.loader import settings

http_client = RequestsClient()
client = APIClient(
    base_url=str(settings.API_URL),
    http_client=http_client
)