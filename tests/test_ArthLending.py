import brownie
from brownie import Wei
from brownie import accounts, ArthLending, ArthArbV1MultiSwap, ERC20Mock
import pytest
from brownie.test import strategy
import hypothesis

ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"

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
def erc20Asset(lender1, admin):
    asset = admin.deploy(ERC20Mock, "token0", "MOCK", lender1, Wei("1000000 ether"))     
    return asset


@pytest.fixture
def ArthArbMultiSwapInst(borrower1):
    return ArthArbV1MultiSwap.deploy(ZERO_ADDRESS, {'from': borrower1})

def test_depost_ether(arthLending, accounts, lender1):
    arthLending.initialize(lender1, 35, {'from': lender1})

    asset = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    amount = 100
    arthLending.deposit(asset, amount, 1, {'from': lender1, 'value': amount})

    assert arthLending.balance() == amount

    arthLending.withdraw(asset, amount, 1, {'from': lender1})

    assert arthLending.balance() == 0

def test_deposit_erc20(arthLending, accounts, lender1, erc20Asset):
    arthLending.initialize(lender1, 35, {'from': lender1})

    asset = erc20Asset.address
    amount = 100
    erc20Asset.approve(arthLending.address, amount, {'from': lender1})
    arthLending.deposit(asset, amount, 1, {'from': lender1})

    assert erc20Asset.balanceOf(arthLending.address) == amount

    arthLending.withdraw(asset, amount, 1, {'from': lender1})

    assert arthLending.balance() == 0

class StateMachine:

    value = strategy('uint256', max_value = Wei("10 ether"))
    #address = strategy('address')
    asset = hypothesis.strategies.sampled_from(["0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"])

    def __init__(cls, accounts, arthLending, ArthArbMultiSwapInst, lender1, borrower1):
        # deploy the contract at the start of the test
        cls.accounts = accounts
        cls.arthLending = arthLending
        cls.ArthArbMultiSwapInst = ArthArbMultiSwapInst
        cls.lender1 = lender1
        cls.borrower1 = borrower1

    def setup(self):
        # zero the deposit amounts at the start of each test run
        self.deposits = {i: 0 for i in self.accounts}

    def rule_flashLoan(self, value, asset):
        if value > 0:
            if(self.arthLending.balance() >= value): 
                self.ArthArbMultiSwapInst.arbitrage(self.arthLending, asset, value, {'from': self.borrower1})
            else:
                with brownie.reverts("There is not enough liquidity available to borrow"):
                    self.ArthArbMultiSwapInst.arbitrage(self.arthLending, asset, value, {'from': self.borrower1})
        else:
            with brownie.reverts("Amount must be greater than 0"):
                self.ArthArbMultiSwapInst.arbitrage(self.arthLending, asset, value, {'from': self.borrower1})

    def invariant(self):
        pass
"""
def test_stateful(arthLending, ArthArbMultiSwapInst, accounts, lender1, borrower1, state_machine):
    arthLending.initialize(accounts[0], 0, {'from': lender1})
    arthLending.deposit("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", Wei("12 ether"), 1, {'from': lender1, "value": Wei("12 ether")})
    state_machine(StateMachine, accounts, arthLending, ArthArbMultiSwapInst, lender1, borrower1)
"""