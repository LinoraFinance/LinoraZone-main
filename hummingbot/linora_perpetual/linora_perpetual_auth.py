import os
from typing import Optional

from linora_py import linora
from linora_py.account.account import linoraAccount
from linora_py.api.api_client import linoraApiClient
from linora_py.environment import PROD, TESTNET, Environment
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, WSRequest



class linoraPerpetualAuth(AuthBase):
    """
    Auth class required by linora Perpetual API
    """
    def __init__(
        self,
        linora_perpetual_l1_address: str,
        linora_perpetual_is_testnet: bool,
        linora_perpetual_l1_private_key: Optional[str] = None,
        linora_perpetual_l2_private_key: Optional[str] = None
    ):
        self._linora_perpetual_l1_address = linora_perpetual_l1_address
        self._linora_perpetual_chain = TESTNET if linora_perpetual_is_testnet else PROD
        self._linora_perpetual_l1_private_key = linora_perpetual_l1_private_key
        self._linora_perpetual_l2_private_key = linora_perpetual_l2_private_key

        self._linora_account: linoraAccount = None
        self._rest_api_client: linoraApiClient = None

    @property
    def linora_account(self):
        if self._linora_account is None:
            self.linora_rest_client
        return self._linora_account

    @property
    def linora_rest_client(self):
        if self._rest_api_client is None:

            env = self._linora_perpetual_chain

            self._rest_api_client = linoraApiClient(
                env=env, 
                logger=None
            )
            self.config = self._rest_api_client.fetch_system_config()
            self._linora_account = linoraAccount(    
                config=self.config,
                l1_address=self._linora_perpetual_l1_address, 
                l1_private_key=self._linora_perpetual_l1_private_key,
                l2_private_key=self._linora_perpetual_l2_private_key
            )

            self._rest_api_client.init_account(self._linora_account)
        return self._rest_api_client

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        self.linora_rest_client._validate_auth()

        headers = self.linora_rest_client.client.headers

        if request.headers is not None:
            headers.update(request.headers)

        request.headers = headers
        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        return request
