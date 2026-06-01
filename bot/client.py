import hmac
import hashlib
import time
import requests
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class BinanceAPIError(Exception):
    def __init__(self, message, status_code, response_body):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = "https://testnet.binancefuture.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _signed_request(self, method: str, endpoint: str, params: dict = None) -> dict:
        if params is None:
            params = {}
        
        params['timestamp'] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        params['signature'] = signature
        url = f"{self.base_url}{endpoint}"
        
        # Safe params for logging (without signature/secret details)
        log_params = {k: v for k, v in params.items() if k not in ['signature']}
        logger.debug(f"Request: {method} {endpoint} params={log_params}")
        
        response = self.session.request(method, url, params=params)
        
        logger.debug(f"Response: {response.status_code} body={response.text}")
        
        if not str(response.status_code).startswith('2'):
            raise BinanceAPIError(
                f"Binance API Error: {response.status_code}",
                status_code=response.status_code,
                response_body=response.text
            )
            
        return response.json()

    def place_order(self, **kwargs) -> dict:
        return self._signed_request("POST", "/fapi/v1/order", params=kwargs)

    def get_exchange_info(self) -> dict:
        url = f"{self.base_url}/fapi/v1/exchangeInfo"
        logger.debug(f"Request: GET /fapi/v1/exchangeInfo")
        response = self.session.get(url)
        logger.debug(f"Response: {response.status_code} body={response.text[:200]}...") # truncated for sanity
        if not str(response.status_code).startswith('2'):
            raise BinanceAPIError(
                f"Binance API Error: {response.status_code}",
                status_code=response.status_code,
                response_body=response.text
            )
        return response.json()
