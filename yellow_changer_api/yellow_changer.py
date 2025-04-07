import hashlib
import hmac
from typing import Optional, Union
import requests
import httpx

from .exceptions import BadRequest, UnsupportedBank, UnsupportedMemo
from .validations import BANKS, format_number


class YellowChanger():
    def __init__(
        self,
        public_api_key: str,
        secret_api_key: str,
        base_url: Union[None, str] = None
    ):
        """
        All you need to pass only public_api_key and secret_api_key

        :param public_api_key: Public API Key obtained from https://yellowchanger.com/auth/register
        :param secret_api_key: Secret API Key obtained from https://yellowchanger.com/auth/register
        :param base_url: BaseURL of API, if domain will be changed
        """
        self.public_api_key = public_api_key
        self.secret_api_key = secret_api_key
        self.base_headers = {
            "Content-Type": "application/json",
            "Y_API_KEY": self.public_api_key
        }
        if not base_url:
            self.base_url = "https://api.yellowchanger.com/"

    def __create_hmac_sha256(self, data: dict, secret_key: str):
        """
        Method for generation signature of request.
        Copied form https://docs.yellowchanger.com/signature

        :param body: Body of request to make a signature
        """
        query_string = "&".join(
            [f"{key}={value}" for key, value in data.items()])
        signature = hmac.new(
            secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return signature

    def __fetch(
        self,
        method: str,
        path: str,
        body: Union[dict, None] = None
    ) -> requests.Response:
        """
        Base request method.
        If request has body, we add signature to request

        :param method: 'GET' or 'POST'
        :param path: path to endpoint
        :param body: body of request
        :return: requests.Response
        """
        headers = self.base_headers.copy()
        url = self.base_url + path

        try:
            if method.upper() == "POST":
                if body is None:
                    raise ValueError("Body of POST request is empty!")

                signature = self.__create_hmac_sha256(
                    body, self.secret_api_key)
                headers["Signature"] = signature
                response = requests.post(url, headers=headers, json=body)

            elif method.upper() == "GET":
                if body:
                    signature = self.__create_hmac_sha256(
                        body, self.secret_api_key)
                    headers["Signature"] = signature
                response = requests.get(url, headers=headers, json=body)

            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

        except requests.exceptions.HTTPError as http_err:
            raise BadRequest(f"HTTP error occurred: {http_err}")

        except Exception as err:
            raise BadRequest(f"An error occurred: {err}")

        if not str(response.status_code).startswith("20"):
            raise BadRequest(
                f"Http status code {response.status_code}: {response.text}"
            )

        return response

    def all_rates(
        self,
        exch_type: str = "yellow",
        commission_crypto_to_rub: float = 0.5,
        commission_crypto_to_crypto: float = 0.5
    ):
        """
        commission = additional commission in percent which is considered
        as your profit, courses will be issued with it taken into account,
        default value 0.5

        exch_type=yellow #rate will fix for 10 minutes (default value)

        exch_type=green #the rate is fixed at the moment payment is received

        Gets all rates

        https://docs.yellowchanger.com/allRates
        :return: Dictionary with all possible exchange rates
        """

        body = {
            "exch_type": exch_type,
            "commission_crypto_to_rub": commission_crypto_to_rub,
            "commission_crypto_to_crypto": commission_crypto_to_crypto
        }
        response = self.__fetch("GET", "trades/allRates", body)
        return response.json()

    def destinations_list(self):
        """
        Gets all destinations list

        https://docs.yellowchanger.com/destinationsList

        :return: Dictionary with all possible exchange destinations
        """
        response = self.__fetch("GET", "trades/destinationsList")
        return response.json()

    def rates_in_direction(
        self,
        direction: str,
        exch_type: str = "yellow",
        commission_crypto_to_rub: float = 0.5,
        commission_crypto_to_crypto: float = 0.5
    ):
        """
        commission = additional commission in percent which is considered
        as your profit, courses will be issued with it taken into account,
        default value 0.5

        exch_type=yellow #rate will fix for 10 minutes (default value)

        exch_type=green #the rate is fixed at the moment payment is received

        Gets all rates in specific direction

        https://docs.yellowchanger.com/ratesInDirection

        :param direction: direction of rate, for example: 'USDT'
        :return: Dictionary with rates in a certain direction
        """
        body = {
            "direction": direction,
            "exch_type": exch_type,
            "commission_crypto_to_rub": commission_crypto_to_rub,
            "commission_crypto_to_crypto": commission_crypto_to_crypto
        }
        response = self.__fetch("GET", "trades/ratesInDirection", body)
        return response.json()

    def get_info(self, uniq_id: str):
        """
        Gets information about trade by uniq_id of trade

        https://docs.yellowchanger.com/getInfo

        :param uniq_id: uniq_id of trade
        :return: Dictionary with all information about transaction
        """
        body = {"uniq_id": uniq_id}
        response = self.__fetch("GET", "trades/getInfo", body)
        return response.json()

    def create_trade(
        self,
        send_name: str,
        get_name: str,
        send_network: str,
        get_network: str,
        get_creds: str,
        send_value: Union[float, None] = None,
        get_value: Union[float, None] = None,
        commission: float = 0.5,
        exch_type: Union[str, None] = "yellow",
        uniq_id: Union[str, None] = None,
        sbpBank: Union[str, None] = None,
        memo: Union[str, None] = None,
        recipientName: Union[str, None] = None,
        testMode: Union[int, None] = None
    ):
        """
        Creates a new trade via the YellowChanger API.
        For details, see: https://docs.yellowchanger.com/createTrade

        Example:
        ```python
        trade = self.create_trade(
            send_name="USDT",
            get_name="RUB",
            send_network="TRC20",
            get_network="RUB",
            get_creds="1234567890123456",
            send_value=100.0,
            exch_type="yellow",
            commission=0.5,
            sbpBank="sbpsber"
        )
        ```

        :param send_name: Currency being sent (e.g. "USDT").
        :param get_name: Currency/asset to be received (e.g. "RUB").
        :param send_network: Network for the currency being sent (e.g. "TRC20").
        :param get_network: Network for the currency being received (e.g. "ERC20").
        :param get_creds: Receiving credentials (address/card/etc.).
        :param send_value: Amount to send (optional).
        :param get_value: Amount to receive (optional). If both are set, the final amount is auto-calculated.
        :param commission: Additional commission in percent (default is 0.5).
        :param exch_type: "yellow" (rate fixed 10 min) or "green" (rate at payment). Defaults to "yellow".
        :param uniq_id: Optional unique ID for this trade.
        :param sbpBank: Optional bank name for SBP if receiving RUB via SBP.
        :param memo: Optional note/memo.
        :param recipientName: Optional recipient's name.
        :param testMode: Optional test mode (1 or 0). Allows emulating exchange without payment.

        :return: Dictionary with API response data about the created trade.
        """

        body = {
            "send_name": send_name,
            "get_name": get_name,
            "send_network": send_network,
            "get_network": get_network,
            "get_creds": get_creds,
            "exch_type": exch_type,
            "commission": commission,
        }
        if uniq_id:
            body["uniq_id"] = str(uniq_id)
        if sbpBank:
            if sbpBank.lower() in BANKS.keys():
                body["sbpBank"] = str(sbpBank)
        if send_value:
            body["send_value"] = format_number(send_value)
        if get_value:
            body["get_value"] = format_number(get_value)
        if memo:
            if get_network in ["TON", "SOL"]:
                body["get_memo"] = str(memo)
            else:
                raise UnsupportedMemo
        if recipientName:
            body["recipientName"] = str(recipientName)
        if testMode is not None:
            if testMode not in [0, 1]:
                raise ValueError("testMode должен быть 0 или 1")
            body["testMode"] = testMode
        response = self.__fetch("POST", "trades/createTrade", body)
        return response.json()

    def cancel_trade(self, uniq_id: str):
        """
        Cancels a exchange by its unique ID.
        For details, see: https://docs.yellowchanger.com/cancelTrade

        :param uniq_id: Unique ID of the trade to cancel.
        :return: Dictionary with API response data about the canceled trade.
        """
        body = {"uniq_id": uniq_id}
        response = self.__fetch("POST", "trades/cancelTrade", body)
        return response.json()

    def change_credentials(self, uniq_id: str, get_creds: str, sbpBank: str = None):
        """
        Changes the receiving credentials for a trade by its unique ID.
        For details, see: https://docs.yellowchanger.com/changeCredentials

        :param uniq_id: Unique ID of the trade to change credentials for.
        :param get_creds: New receiving credentials (address/card/etc.).
        :param sbpBank: Optional bank name for SBP if receiving RUB via SBP.
        :return: Dictionary with API response data about the changed credentials.
        """
        body = {"uniq_id": str(uniq_id), "get_creds": str(get_creds)}
        if sbpBank:
            if sbpBank.lower() in BANKS.keys():
                body["sbpBank"] = str(sbpBank)
            else:
                raise UnsupportedBank
        response = self.__fetch("POST", "trades/changeCredentials", body)
        return response.json()

    def emulate_payment(
        self,
        uniq_id: str,
        paidAmount: str,
        withdrawStatus: str,
        depositStatus: str,
        isInvalidRequisites: int
    ):
        """
        Emulates a payment for a trade by its unique ID.
        For details, see: https://docs.yellowchanger.com/emulatePayment

        :param uniq_id: Unique ID of the trade to emulate payment for
        :param paidAmount: Amount paid by user
        :param withdrawStatus: Withdrawal status. Possible values:
            - withdrawing: withdrawal in progress
            - error: error occurred
            - amlblock: AML block
            - sent: successfully sent
            - wait_pay: waiting for payment
        :param depositStatus: Deposit status. Possible values:
            - user_paid: user has paid
            - confirmations: waiting for confirmations
            - error: error occurred
            - amlblock: AML block
            - wait_pay: waiting for payment
        :param isInvalidRequisites: Emulates invalid credentials provided (1 or 0)
        :return: Dictionary with API response data about the emulated payment
        """
        body = {
            "uniqId": uniq_id,
            "paidAmount": paidAmount,
            "withdrawStatus": withdrawStatus,
            "depositStatus": depositStatus,
            "isInvalidRequisites": isInvalidRequisites
        }
        response = self.__fetch("POST", "trades/emulatePayment", body)
        return response.json()


class AsyncYellowChanger():
    def __init__(
        self,
        public_api_key: str,
        secret_api_key: str,
        base_url: Optional[str] = None
    ):
        """
        All you need to pass only public_api_key and secret_api_key

        :param public_api_key: Public API Key obtained from yellowchanger.com
        :param secret_api_key: Secret API Key obtained from yellowchanger.com
        :param base_url: BaseURL of API, if domain will be changed
        """
        self.public_api_key = public_api_key
        self.secret_api_key = secret_api_key
        self.base_headers = {
            "Content-Type": "application/json",
            "Y_API_KEY": self.public_api_key
        }
        if not base_url:
            self.base_url = "https://api.yellowchanger.com/"

    def __create_hmac_sha256(self, data: dict, secret_key: str):
        """
        Method for generation signature of request.

        :param body: Body of request to make a signature
        """
        query_string = "&".join(
            [f"{key}={value}" for key, value in data.items()])
        signature = hmac.new(
            secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

        return signature

    async def __fetch(
        self,
        method: str,
        path: str,
        body: Optional[dict] = None
    ) -> httpx.Response:
        """
        Base request method.
        If request has body, we add signature to request

        :param method: 'GET' or 'POST'
        :param path: path to endpoint
        :param body: body of request
        :return: httpx.Response
        """
        headers = self.base_headers.copy()
        url = self.base_url + path

        try:
            async with httpx.AsyncClient() as client:
                if method.upper() == "POST":
                    if body is None:
                        raise ValueError("Body of POST request is empty!")

                    signature = self.__create_hmac_sha256(
                        body, self.secret_api_key)
                    headers["Signature"] = signature
                    response = await client.post(url, headers=headers, json=body)

                elif method.upper() == "GET":
                    if body:
                        signature = self.__create_hmac_sha256(
                            body, self.secret_api_key)
                        headers["Signature"] = signature
                        response = await client.get(url, headers=headers, json=body)
                    else:
                        response = await client.get(url, headers=headers)

                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")

                if not str(response.status_code).startswith("20"):
                    raise BadRequest(
                        f"Http status code {response.status_code}: {response.text}"
                    )

                return response

        except httpx.HTTPError as http_err:
            raise BadRequest(f"HTTP error occurred: {http_err}")

        except Exception as err:
            raise BadRequest(f"An error occurred: {err}")

    async def all_rates(
        self,
        exch_type: str = "yellow",
        commission_crypto_to_rub: float = 0.5,
        commission_crypto_to_crypto: float = 0.5
    ):
        """
        Gets all rates

        https://docs.yellowchanger.com/allRates
        :return: Dictionary with all possible exchange rates
        """
        body = {
            "exch_type": exch_type,
            "commission_crypto_to_rub": commission_crypto_to_rub,
            "commission_crypto_to_crypto": commission_crypto_to_crypto
        }
        response = await self.__fetch("GET", "trades/allRates", body)
        return response.json()

    async def destinations_list(self):
        """
        Gets all destinations list

        https://docs.yellowchanger.com/destinationsList
        :return: Dictionary with all possible exchange destinations
        """
        response = await self.__fetch("GET", "trades/destinationsList")
        return response.json()

    async def rates_in_direction(
        self,
        direction: str,
        exch_type: str = "yellow",
        commission_crypto_to_rub: float = 0.5,
        commission_crypto_to_crypto: float = 0.5
    ):
        """
        Gets all rates in specific direction

        https://docs.yellowchanger.com/ratesInDirection
        :param direction: direction of rate, for example: 'USDT'
        :return: Dictionary with rates in a certain direction
        """
        body = {
            "direction": direction,
            "exch_type": exch_type,
            "commission_crypto_to_rub": commission_crypto_to_rub,
            "commission_crypto_to_crypto": commission_crypto_to_crypto
        }
        response = await self.__fetch("GET", "trades/ratesInDirection", body)
        return response.json()

    async def get_info(self, uniq_id: str):
        """
        Gets information about trade by uniq_id of trade

        https://docs.yellowchanger.com/getInfo
        :param uniq_id: uniq_id of trade
        :return: Dictionary with all information about transaction
        """
        body = {"uniq_id": uniq_id}
        response = await self.__fetch("GET", "trades/getInfo", body)
        return response.json()

    async def create_trade(
        self,
        send_name: str,
        get_name: str,
        send_network: str,
        get_network: str,
        get_creds: str,
        send_value: Optional[float] = None,
        get_value: Optional[float] = None,
        commission: float = 0.5,
        exch_type: Optional[str] = "yellow",
        uniq_id: Optional[str] = None,
        sbpBank: Optional[str] = None,
        memo: Optional[str] = None,
        recipientName: Optional[str] = None,
        testMode: Optional[int] = None
    ):
        """
        Creates a new trade via the YellowChanger API.
        """
        body = {
            "send_name": send_name,
            "get_name": get_name,
            "send_network": send_network,
            "get_network": get_network,
            "get_creds": get_creds,
            "exch_type": exch_type,
            "commission": commission,
        }
        if uniq_id:
            body["uniq_id"] = str(uniq_id)
        if sbpBank:
            if sbpBank.lower() in BANKS.keys():
                body["sbpBank"] = str(sbpBank)
        if send_value:
            body["send_value"] = format_number(send_value)
        if get_value:
            body["get_value"] = format_number(get_value)
        if memo:
            if get_network in ["TON", "SOL"]:
                body["get_memo"] = str(memo)
            else:
                raise UnsupportedMemo
        if recipientName:
            body["recipientName"] = str(recipientName)
        if testMode is not None:
            if testMode not in [0, 1]:
                raise ValueError("testMode должен быть 0 или 1")
            body["testMode"] = testMode
        response = await self.__fetch("POST", "trades/createTrade", body)
        return response.json()

    async def cancel_trade(self, uniq_id: str):
        """
        Cancels a exchange by its unique ID.
        """
        body = {"uniq_id": uniq_id}
        response = await self.__fetch("POST", "trades/cancelTrade", body)
        return response.json()

    async def change_credentials(self, uniq_id: str, get_creds: str, sbpBank: Optional[str] = None):
        """
        Changes the receiving credentials for a trade.
        """
        body = {"uniq_id": str(uniq_id), "get_creds": str(get_creds)}
        if sbpBank:
            if sbpBank.lower() in BANKS.keys():
                body["sbpBank"] = str(sbpBank)
            else:
                raise UnsupportedBank
        response = await self.__fetch("POST", "trades/changeCredentials", body)
        return response.json()

    async def emulate_payment(
        self,
        uniq_id: str,
        paidAmount: str,
        withdrawStatus: str,
        depositStatus: str,
        isInvalidRequisites: int
    ):
        """
        Emulates a payment for a trade by its unique ID.
        """
        body = {
            "uniqId": uniq_id,
            "paidAmount": paidAmount,
            "withdrawStatus": withdrawStatus,
            "depositStatus": depositStatus,
            "isInvalidRequisites": isInvalidRequisites
        }
        response = await self.__fetch("POST", "trades/emulatePayment", body)
        return response.json()
