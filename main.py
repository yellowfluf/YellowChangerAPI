from yellow_changer_api import YellowChanger


def main():
    public_api_key = "your_public_key"
    secret_api_key = "your_private_key"

    yellow_changer = YellowChanger(public_api_key, secret_api_key)

    rates = yellow_changer.all_rates(
        commission_crypto_to_rub=0.5,
        commission_crypto_to_crypto=0.5
    )
    print(rates)

    destinations_list = yellow_changer.destinations_list()
    print(destinations_list)

    rates_in_direction_USDT = yellow_changer.rates_in_direction(
        'USDT',
        commission_crypto_to_rub=0.5,
        commission_crypto_to_crypto=0.5
    )
    print(rates_in_direction_USDT)

    trade = yellow_changer.create_trade(
        send_name='USDT',
        get_name='USDT',
        send_value=100,
        send_network='TRC20',
        get_network='ERC20',
        get_creds='0x4c0101a8CB61766bbE110BB530C03A58383e3545',
        exch_type='yellow',
        commission=0.5
    )

    trade_uniq_id = trade.get('uniq_id')

    trade_info = yellow_changer.get_info(trade_uniq_id)
    print(trade_info)

    emulated_payment = yellow_changer.emulate_payment(
        uniq_id=trade_uniq_id,
        paidAmount="100.50",
        withdrawStatus="sent",
        depositStatus="user_paid",
        isInvalidRequisites=0
    )
    print(emulated_payment)

    cancelled_trade = yellow_changer.cancel_trade(trade_uniq_id)
    print(cancelled_trade)


if __name__ == '__main__':
    main()
