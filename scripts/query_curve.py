import sys
from brownie import *
import time

token_list = {
    "DAI": {"address":"0x6b175474e89094c44da98b954eedeac495271d0f", "decimals":18},
    "USDC": {"address":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "decimals":6},
    "USDT": {"address":"0xdac17f958d2ee523a2206206994597c13d831ec7", "decimals":6},
    "wBTC": {"address":"0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", "decimals":8},
    "renBTC": {"address":"0xeb4c2781e4eba804ce9a9803c67d0893436bb27d", "decimals":8},
    "BUSD": {"address":"0x4fabb145d64652a948d72533023f6e7a623c7c53", "decimals":18},
    "TUSD": {"address":"0x0000000000085d4780b73119b644ae5ecd22b376", "decimals":18},
    "EURS": {"address":"0xdB25f211AB05b1c97D595516F45794528a807ad8", "decimals":2},

    "aETH": {"address":"0xE95A203B1a91a908F9B9CE46459d101078c2c3cb",  "decimals":18},    
    "ETH": {"address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  "decimals":18},
}
"""
pool_coins = {
    "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "BUSD": "0x4fabb145d64652a948d72533023f6e7a623c7c53",
    "TUSD": "0x0000000000085d4780b73119b644ae5ecd22b376",
    "sUSD": "0x57ab1ec28d129707052df4df418d58a2d46d5f51",
    "ETH": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "stETH": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
    "sETH": "0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb",
    "renBTC": "0xeb4c2781e4eba804ce9a9803c67d0893436bb27d",
    "wBTC": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
    "sBTC": "0xfe18be6b3bd88a2d2a7f928d00292e7a9963cfc6",
    "EURS": "0xdB25f211AB05b1c97D595516F45794528a807ad8",
    "sEUR": "0xD71eCFF9342A5Ced620049e616c5035F1dB98620",
}
"""
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

active_network = network.show_active()

curve_addressprovider= None
curve_registry_addr = None
curve_poolinfo_addr = None

if active_network == "kovan":
    curve_addressprovider=AddressProvider.at("TODO")
elif active_network == "mainnet":
    curve_addressprovider=AddressProvider.at("0x0000000022D53366457F9d5E68Ec105046FC4383")
else:
    print("network {} not supported".format(active_network))
    sys.exit()

curve_registry_addr = curve_addressprovider.get_registry()
curve_poolinfo_addr = curve_addressprovider.get_address(1)
curve_swaps_addr = curve_addressprovider.get_address(2)

registry = Registry.at(curve_registry_addr)
poolinfo = PoolInfo.at(curve_poolinfo_addr)
swaps = Swaps.at(curve_swaps_addr)


def get_outputs_for_input(from_token, amount):
    out_amounts = []
    _from = token_list[from_token]["address"]
    for to_token in token_list:
        _to = token_list[to_token]["address"]
        if _from == _to:
            continue
        (pool_addr,rate) = swaps.get_best_rate(_from, _to, amount)
        if pool_addr == ZERO_ADDRESS:
            continue
        try:
            balances = registry.get_underlying_balances(pool_addr)
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
        print(f"balances: {balances}")

        coins = registry.get_underlying_coins(pool_addr)
        print(f"coins: {coins}")
        i = 0
        reserve_from  = 0
        reserve_to = 0
        for i, coin in enumerate(coins, start=0):
            if coin == _from:
                reserve_from = balances[i]
            if coin == _to:
                reserve_to = balances[i]

        #print(f"rate {from_token}:{_from}, {to_token}:{_to}, pool_addr:{pool_addr} rate:{rate}")
        out_amounts.append({"pool":pool_addr, "swap0-1": rate, "token0": from_token, "token1": to_token, "reserve0": reserve_from, "reserve1": reserve_to})
        #out_amounts.append({"swap0-1": rate, "token0": from_token, "token1": to_token})
    print(out_amounts)
    return out_amounts

def get_output_for_inputs(to_token, from_tokens_amounts):
    out_amounts = []
    _to = token_list[to_token]["address"]
    for swap0 in from_tokens_amounts:
        from_token = swap0["token1"]
        _from = token_list[from_token]["address"]
        if _from == _to:
            continue
        amount = swap0["swap0-1"]            
        (pool_addr,rate) = swaps.get_best_rate(_from, _to, amount)
        if pool_addr == ZERO_ADDRESS:
            continue

        try:
            balances = registry.get_underlying_balances(pool_addr)
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
        print(f"balances: {balances}")

        coins = registry.get_underlying_coins(pool_addr)
        print(f"coins: {coins}")
        i = 0
        reserve_from  = 0
        reserve_to = 0
        for i, coin in enumerate(coins, start=0):
            if coin == _from:
                reserve_from = balances[i]
            if coin == _to:
                reserve_to = balances[i]

        #print(f"rate {from_token}:{_from}, {to_token}:{_to}, pool_addr:{pool_addr} rate:{rate}")
        out_amounts.append({"pool":pool_addr, "swap0-1": rate, "token0": from_token, "token1": to_token, "reserve0": reserve_from, "reserve1": reserve_to})
    print(out_amounts)
    return out_amounts

def showPool(i):
    pool_addr = registry.pool_list(i)
    pinfo = poolinfo.get_pool_info(pool_addr)
    #token0 = interface.IERC20(pair.token0())
    #token1 = interface.IERC20(pair.token1())
    # print(f"pair {pair.name()}, {pair.symbol()}, {pair.token0()}, {pair.token1()} {reserve0/1E18} {reserve1/1E18} {blockTimestampLast}")
    print(pinfo)

def showPools(i):
    for j in range (i):
        showPool(j)
    time.sleep(1)
    
def main():
    #get_best_rate("DAI", "USDC", Wei("10 ether"))
    get_best_rates_all("DAI", Wei("10 ether"))