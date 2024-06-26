import sys
from brownie import *


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



def main():
    accounts.load("account1")    
    ArthCurveSwap.deploy(curve_registry_addr, {'from':accounts[0]})