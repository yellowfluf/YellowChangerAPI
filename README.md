# YellowChangerAPI

`YellowChangerAPI` is a Python library for interacting with the [YellowChanger](https://yellowchanger.com) service API. The library allows you to get exchange rates, create trades, and get information about trades.

## Installation

To install the library, use the following command:

```sh
pip install yellowchangerapi
```

## Usage

Example of using the library:

```python
from yellow_changer_api import YellowChanger

def main():
    public_api_key = "your_public_api_key"
    secret_api_key = "your_secret_api_key"

    yellow_changer = YellowChanger(public_api_key, secret_api_key)

    # Get all rates
    rates = yellow_changer.all_rates()
    print(rates)

    # Get destinations list
    destinations_list = yellow_changer.destinations_list()
    print(destinations_list)

    # Get rates in direction USDT
    rates_in_direction_USDT = yellow_changer.rates_in_direction('USDT')
    print(rates_in_direction_USDT)

    # Create a trade
    trade = yellow_changer.create_trade(
        send_name='USDT',
        get_name='USDT',
        send_value=100,
        send_network='TRC20',
        get_network='ERC20',
        get_creds='0x4c...'
    )

    trade_uniq_id = trade.get('uniq_id')

    # Get trade information
    trade_info = yellow_changer.get_info(trade_uniq_id)
    print(trade_info)

if __name__ == '__main__':
    main()
```

## Methods

### `all_rates()`

Gets all exchange rates.

**Example:**
```python
rates = yellow_changer.all_rates()
print(rates)
```

### `destinations_list()`

Gets the list of all destinations.

**Example:**
```python
destinations = yellow_changer.destinations_list()
print(destinations)
```

### `rates_in_direction(direction: str)`

Gets all exchange rates in a specific direction.

**Parameters:**
- `direction` (str): The direction of the rate, for example, 'USDT'.

**Example:**
```python
rates = yellow_changer.rates_in_direction('USDT')
print(rates)
```

### `get_info(uniq_id: str)`

Gets information about a trade by the unique ID of the trade.

**Parameters:**
- `uniq_id` (str): The unique ID of the trade.

**Example:**
```python
info = yellow_changer.get_info('your_unique_id')
print(info)
```

### `create_trade(*args, **kwargs)`

Creates a new trade based on the provided parameters.

**Example for crypro:**
```python
trade = yellow_changer.create_trade(
    send_name='USDT',
    get_name='USDT',
    send_value=100,
    send_network='TRC20',
    get_network='ERC20',
    get_creds='0x4c...'
)
print(trade)
```

**Example for bank:**
```python
trade = yellow_changer.create_trade(
    send_name="USDT",
    get_name="RUB",
    send_value=100,
    send_network="TRC20",
    get_network="RUB",
    get_creds="1234567890123456",
    sbpBank="sbpsber"
)
print(trade)
```