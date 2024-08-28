from typing import List, Dict, Union, Optional

from pydantic import BaseModel, field_validator, RootModel


class ConversionRate(BaseModel):
    name: str
    rate: Union[int, float]

class NetWorkWithdraw(BaseModel):
    network: str
    fee: Union[int, float]
    min_withdraw: Union[int, float]

class NetWorkDeposit(BaseModel):
    network: str
    fee: Union[int, float]
    min_deposit: Union[int, float]

class Rate(BaseModel):
    currency: str
    name: str
    withdraw_networks: List[NetWorkWithdraw]
    deposit_networks: List[NetWorkDeposit]
    conversion_rates: List[ConversionRate]

    @field_validator('conversion_rates', mode='before')
    def convertion_rates_check(cls, data: Dict) -> list:
        res = []
        for values in data.items():
            res.append(ConversionRate.model_validate({'name': values[0], 'rate': values[1]}))
        return res

class RatesList(RootModel):
    root: List[Rate]

class Trade(BaseModel):
    send_name: str
    send_network: str
    get_network: str
    uniq_id: str
    status: int
    payment_wallet: str
    userPaidHash: str
    ourHash: str
    get_creds: str
    network_commission: Union[int, float]
    date: int
    time_expire: int
    send_value: str
    get_value: str

class Limit(BaseModel):
    min_amount: Union[int, float]
    max_amount: Union[int, float]

class Comission(BaseModel):
    fee_amount: Union[int, float]

class Destination(BaseModel):
    currency: str
    network: str
    limit: Limit
    commission: Optional[Comission] = None

class Destinations(BaseModel):
    payin: List[Destination]
    payout: List[Destination]
