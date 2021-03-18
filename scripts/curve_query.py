import sys
from brownie import *
import time

active_network = network.show_active()

curve_addressprovider= None
curve_registry_addr = None
curve_poolinfo_addr = None

if active_network == "kovan":
    curve_addressprovider_addr = "TODO"
elif active_network == "mainnet":
    curve_addressprovider_addr = "0x0000000022D53366457F9d5E68Ec105046FC4383"
else:
    print("network {} not supported".format(active_network))
    sys.exit()

curve_addressprovider=AddressProvider.at("0x0000000022D53366457F9d5E68Ec105046FC4383")
curve_registry_addr = curve_addressprovider.get_registry()
curve_poolinfo_addr = curve_addressprovider.get_address(1)

registry = Registry.at(curve_registry_addr)
poolinfo = PoolInfo.at(curve_poolinfo_addr)

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
    pass