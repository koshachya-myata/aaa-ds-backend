import io
import requests
from urllib.parse import urljoin


class ImageProviderClient:
    def __init__(self, service_url: str, timeout: int = 5):
        self.service_url = service_url
        self.timeout = timeout
    
    def get_image(self, img_id: str) -> io.BytesIO | None:
        url = urljoin(self.service_url, img_id)
        print(url)
        try:
            response = requests.get(url, stream=True, timeout=self.timeout)
            if response.status_code != 200:
                print(response.status_code)
                return None
        except requests.Timeout:
            return None
        return io.BytesIO(response.content)



