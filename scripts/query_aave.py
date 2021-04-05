import sys
from brownie import *
import time

aveLendingPoolAddressesProviderAddress = "0x24a42fD28C976A61Df5D00D0599C34c4f90748c8"

token_list = {
    "DAI": {"address":"0x6b175474e89094c44da98b954eedeac495271d0f", "decimals":18},
    "USDC": {"address":"0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "decimals":6},
    "USDT": {"address":"0xdac17f958d2ee523a2206206994597c13d831ec7", "decimals":6},
    "wBTC": {"address":"0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", "decimals":8},
    "BUSD": {"address":"0x4fabb145d64652a948d72533023f6e7a623c7c53", "decimals":18},
    "TUSD": {"address":"0x0000000000085d4780b73119b644ae5ecd22b376", "decimals":18},
    "ETH": {"address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",  "decimals":18},
}

aaveProvider = interface.ILendingPoolAddressesProvider(aveLendingPoolAddressesProviderAddress)
aavePoolAddr = aaveProvider.getLendingPool()
lendingPool = interface.ILendingPool(aavePoolAddr)


def print_reserve(reserveData):
    totalLiquidity, availableLiquidity, totalBorrowsFixed,totalBorrowsVariable, liquidityRate, variableBorrowRate, fixedBorrowRate, averageFixedBorrowRate, utilizationRate, liquidityIndex, variableBorrowIndex, aTokenAddress, lastUpdateTimestamp =  reserveData
    print(f"totalLiquidity:{totalLiquidity} availableLiquidity:{availableLiquidity} fixedBorrowRate:{fixedBorrowRate}\n")

def main():
    for token in token_list:
        reserveData = lendingPool.getReserveData(token_list[token]["address"])
        print(f"{token}: {reserveData}\n")
        print_reserve(reserveData)
