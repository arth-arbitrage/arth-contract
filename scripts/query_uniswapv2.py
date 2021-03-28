import sys
from brownie import *
import time
from pprint import pprint
token_list = {
    "WETH": {"address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "decimals":18 },
    "DAI": {"address":"0x6b175474e89094c44da98b954eedeac495271d0f", "decimals":18},
    "USDC": {"address":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "decimals":6},
    "USDT": {"address":"0xdac17f958d2ee523a2206206994597c13d831ec7", "decimals":6},
    "wBTC": {"address":"0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", "decimals":8},
    "renBTC": {"address":"0xeb4c2781e4eba804ce9a9803c67d0893436bb27d", "decimals":8},
    "BUSD": {"address":"0x4fabb145d64652a948d72533023f6e7a623c7c53", "decimals":18},
    "TUSD": {"address":"0x0000000000085d4780b73119b644ae5ecd22b376", "decimals":18},
    "EURS": {"address":"0xdB25f211AB05b1c97D595516F45794528a807ad8", "decimals":2},
    "VID": {"address": "0x2c9023bbc572ff8dc1228c7858a280046ea8c9e5", "decimals":2},
}
"""
{
    "sUSD": "0x57ab1ec28d129707052df4df418d58a2d46d5f51",
    "ETH": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "stETH": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",

    "sEUR": "0xD71eCFF9342A5Ced620049e616c5035F1dB98620",
    "aETH": "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb"
    "sBTC": "0xfe18be6b3bd88a2d2a7f928d00292e7a9963cfc6",
    "sETH": "0x5e74C9036fb86BD7eCdcb084a0673EFc32eA31cb",
}
"""

# Address is common across all networks
factory = interface.IUniswapV2Factory("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f")
router = interface.IUniswapV2Router02("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

def token_name(token_address):
    for token in token_list:
        if token_list[token]["address"] == token_address:
            return token

def showPair(i):
    pair_addr = factory.allPairs(i)
    pair = interface.IUniswapV2Pair(pair_addr)
    #token0 = interface.IERC20(pair.token0())
    #token1 = interface.IERC20(pair.token1())
    (reserve0, reserve1, blockTimestampLast) = pair.getReserves()
    print(f"pair {pair.name()}, {pair.symbol()}, {pair.token0()}, {pair.token1()} {reserve0/1E18} {reserve1/1E18} {blockTimestampLast}")

def get_outputs_for_input(from_token, amount):
    _from = token_list[from_token]["address"]
    token_path = []
    out_amounts = []
    for to_token in token_list:
        _to = token_list[to_token]["address"]
        if _from == _to:
            continue
        token_path= [_from]
        token_path.append(_to)
        try:
            pair_addr = factory.getPair(_from, _to)
            pair = interface.IUniswapV2Pair(pair_addr)
            (reserve0, reserve1, blockTimestampLast) = pair.getReserves()
            token0 = pair.token0()
            #token1 = pair.token1()
            (reserve_from, reserve_to) = (reserve0, reserve1) if _from.lower() == token0.lower() else (reserve1, reserve0)
            out_amount = router.getAmountsOut(amount, token_path)
            decimals0 = token_list[from_token]["decimals"]
            decimals1 = token_list[to_token]["decimals"]

            out_amounts.append({"swap0-1": out_amount[1], "token0": from_token, "token1": to_token, "reserve0": reserve_from, "reserve1": reserve_to})
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
            #pass
    pprint(out_amounts)
    return out_amounts

def get_output_for_inputs(to_token, from_tokens_amounts):
    token_path = []
    out_amounts = []
    _to = token_list[to_token]["address"]    
    for swap0 in from_tokens_amounts:
        from_token = swap0["token1"]
        amount = swap0["swap0-1"]
        _from = token_list[from_token]["address"]
        if _from == _to:
            continue
        token_path= [_from]
        token_path.append(_to)
        try:
            pair_addr = factory.getPair(_from, _to)
            pair = interface.IUniswapV2Pair(pair_addr)
            (reserve0, reserve1, blockTimestampLast) = pair.getReserves()
            token0 = pair.token0()
            #token1 = pair.token1()
            (reserve_from, reserve_to) = (reserve0, reserve1) if _from.lower() == token0.lower() else (reserve1, reserve0)
            out_amount = router.getAmountsOut(amount, token_path)
            decimals0 = token_list[from_token]["decimals"]
            decimals1 = token_list[to_token]["decimals"]

            out_amounts.append({"swap1-0":out_amount[1], "swap1-0_deci":out_amount[1]/10**decimals1, "reserve0":reserve_from, "token1": to_token, "reserve1": reserve_to})
        except Exception as e:
            print('Failed to upload to ftp: '+ str(e))
            #pass
    pprint(out_amounts)


def showPairs(i):
    for j in range (i):
        showPair(j)
    time.sleep(1)
    
def main():
    pass