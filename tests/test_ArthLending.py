import brownie
from brownie import Wei
from brownie import accounts, ArthLending, ArthBorrowerMock
import pytest
from brownie.test import strategy
import hypothesis

@pytest.fixture(scope="session")
def lender1(accounts):
    yield accounts[0]

@pytest.fixture(scope="session")
def borrower1(accounts):
    yield accounts[1]


@pytest.fixture
def arthLending(lender1):
    return lender1.deploy(ArthLending)

@pytest.fixture
def arthBorrowerMock(borrower1):
    return ArthBorrowerMock.deploy({'from': borrower1})

def test_initialize(arthLending, accounts, lender1):
    arthLending.initialize(lender1, 35, {'from': lender1})
    assert arthLending.lendingAddress() == accounts[0]

    asset = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    amount = 100
    arthLending.deposit(asset, amount, 1, {'from': lender1, 'value': amount})

    assert arthLending.balance() == amount

    arthLending.withdraw(asset, amount, 1, {'from': lender1})

    assert arthLending.balance() == 0

class StateMachine:

    value = strategy('uint256', max_value = Wei("10 ether"))
    #address = strategy('address')
    asset = hypothesis.strategies.sampled_from(["0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"])

    def __init__(cls, accounts, arthLending, arthBorrowerMock, lender1, borrower1):
        # deploy the contract at the start of the test
        cls.accounts = accounts
        cls.arthLending = arthLending
        cls.arthBorrowerMock = arthBorrowerMock
        cls.lender1 = lender1
        cls.borrower1 = borrower1

    def setup(self):
        # zero the deposit amounts at the start of each test run
        self.deposits = {i: 0 for i in self.accounts}

    def rule_flashLoan(self, value, asset):
        if value > 0:
            if(self.arthLending.balance() >= value): 
                self.arthBorrowerMock.arbitrage(self.arthLending, asset, value, {'from': self.borrower1})
            else:
                with brownie.reverts("There is not enough liquidity available to borrow"):
                    self.arthBorrowerMock.arbitrage(self.arthLending, asset, value, {'from': self.borrower1})
        else:
            with brownie.reverts("Amount must be greater than 0"):
                self.arthBorrowerMock.arbitrage(self.arthLending, asset, value, {'from': self.borrower1})

    def invariant(self):
        pass

def test_stateful(arthLending, arthBorrowerMock, accounts, lender1, borrower1, state_machine):
    arthLending.initialize(accounts[0], 0, {'from': lender1})
    arthLending.deposit("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", Wei("12 ether"), 1, {'from': lender1, "value": Wei("12 ether")})
    state_machine(StateMachine, accounts, arthLending, arthBorrowerMock, lender1, borrower1)
