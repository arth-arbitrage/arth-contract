# test ArthLending + ArthArbitrage with multi swap

import brownie
from brownie import Wei
from brownie import accounts, ArthLending, SwapWrapArthV1, ArthArbV1MultiSwap, ERC20Mock, ArthDexV1Pair
import pytest
from brownie.test import strategy
import hypothesis

curve_addressprovider="0x0000000022D53366457F9d5E68Ec105046FC4383"

@pytest.fixture(scope="session")
def admin(accounts):
    yield accounts[0]

@pytest.fixture(scope="session")
def lender1(accounts):
    yield accounts[1]

@pytest.fixture(scope="session")
def borrower1(accounts):
    yield accounts[2]

@pytest.fixture
def arthLending(lender1):
    return lender1.deploy(ArthLending)

@pytest.fixture
def numPairsAndAssets(lender1):
    return 3


@pytest.fixture
def ArthMultiSwapV1Inst(borrower1, lender1):
    return borrower1.deploy(ArthArbV1MultiSwap, curve_addressprovider)

@pytest.fixture
def ArthLendingInst(lender1):
    arthLending = lender1.deploy(ArthLending)
    arthLending.initialize(lender1, 0)
    return arthLending


@pytest.fixture
def Erc20Assets(admin, lender1, numPairsAndAssets):
    assets = [admin.deploy(ERC20Mock, "token"+str(i), "MOCK"+str(i), lender1, Wei("1000000 ether")) for i in range(0, numPairsAndAssets)]     
    return assets

@pytest.fixture
def SwapPairs(Erc20Assets, admin, lender1, numPairsAndAssets):
    swapPairs = [admin.deploy(ArthDexV1Pair) for i in range(0,numPairsAndAssets)]     
    for num, swapPair in enumerate(swapPairs, start=0):
        token0 = Erc20Assets[num]
        token1 = Erc20Assets[(num+1)%numPairsAndAssets]
        swapPair.initialize(token0.address, token1.address)
        token0.transfer(swapPair.address, Wei("1000 ether"), {"from":lender1})
        token1.transfer(swapPair.address, Wei("1000 ether"), {"from":lender1})
        swapPair.sync()
    return swapPairs

@pytest.fixture
def SwapWrappperArth(admin, SwapPairs):
    return admin.deploy(SwapWrapArthV1)     


class StateMachine:

    value = strategy('uint256', min_value = Wei("1 ether"), max_value = Wei("10 ether"))
    #address = strategy('address') 

    def __init__(cls, accounts,admin, lender1, borrower1, ArthMultiSwapV1, ArthArbSwapWrapper, SwapPairs, Erc20Assets):
        # deploy the contract at the start of the test
        cls.accounts = accounts
        cls.arthLending = arthLending
        cls.ArthMultiSwapV1 = ArthMultiSwapV1
        cls.admin = admin
        cls.lender1 = lender1
        cls.borrower1 = borrower1
        cls.path = [SwapWrapArthV1.address, SwapPairs[0].address, Erc20Assets[0].address, SwapWrapArthV1.address, SwapPairs[1].address, Erc20Assets[1].address, SwapWrapArthV1.address, SwapPairs[2].address, Erc20Assets[2].address]

    def setup(self):
        # zero the deposit amounts at the start of each test run
        # self.deposits = {i: 0 for i in self.accounts}
        pass

    def rule_Exchange(self, value):
        pass

    def invariant(self):
        pass

def test_exchange(accounts, admin, lender1, borrower1, ArthMultiSwapV1Inst, SwapWrappperArth, SwapPairs, Erc20Assets):
    value = Wei("2 ether")
    reserve = Wei("100 ether")
    
    #loan cusion. remove
    Erc20Assets[0].transfer(ArthMultiSwapV1Inst.address, Wei("10 ether"), {"from":lender1})

    ArthMultiSwapV1Inst.exchange(SwapWrappperArth.address, SwapPairs[0].address, Erc20Assets[0].address, Erc20Assets[1].address, value, value )
    assert(Erc20Assets[0].balanceOf(ArthMultiSwapV1Inst.address) ==   Wei("8 ether")) 
    assert(Erc20Assets[1].balanceOf(ArthMultiSwapV1Inst.address) ==   Wei("2 ether")) 

    ArthMultiSwapV1Inst.exchange(SwapWrappperArth.address, SwapPairs[0].address, Erc20Assets[1].address, Erc20Assets[0].address, value, value ) 
