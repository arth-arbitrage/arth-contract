import sys
from brownie import *
import time
token_list = {
    "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f",
    "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7"
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
    "aETH": "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb"
}

# Address is common across all networks
factory = interface.IUniswapV2Factory("0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f")
router = interface.IUniswapV2Router02("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")

def showPair(i):
    pair_addr = factory.allPairs(i)
    pair = interface.IUniswapV2Pair(pair_addr)
    #token0 = interface.IERC20(pair.token0())
    #token1 = interface.IERC20(pair.token1())
    (reserve0, reserve1, blockTimestampLast) = pair.getReserves()
    print(f"pair {pair.name()}, {pair.symbol()}, {pair.token0()}, {pair.token1()} {reserve0/1E18} {reserve1/1E18} {blockTimestampLast}")

def get_best_rates_all(from_token, amount):
    _from = token_list[from_token]
    token_path = [_from]
    for to_token in token_list:
        _to = token_list[to_token]
        if _from == _to:
            continue
        token_path.append(_to)

    amounts = router.getAmountsOut(amount, token_path)
    print(f"amount {amounts}")


def showPairs(i):
    for j in range (i):
        showPair(j)
    time.sleep(1)
    
def main():
    pass