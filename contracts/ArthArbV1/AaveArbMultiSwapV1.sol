pragma solidity ^0.6.6;

import "./SwapWraps/IArbV1SwapWrap.sol";
import "../aave/FlashLoanReceiverBase.sol";
import "../aave/ILendingPoolAddressesProvider.sol";
import "../aave/ILendingPool.sol";

contract AaveArbMultiSwapV1 is FlashLoanReceiverBase {
    // TODO :remove constructor and pass as parameter
    constructor(address _addressProvider) FlashLoanReceiverBase(_addressProvider) public {}
    
    function executeOperation(address _reserve, uint256 _amount, uint256 _fee, bytes calldata _params) external override {
        
        // swap
        address[] memory path;
        (path) = abi.decode(_params, (address[]));

        require(path.length >= 4, 'ArthArbV1MultiSwap: INVALID_PATH');
        address token0 = _reserve;
        for (uint i = 0; i <  path.length; i=i+4) {
            _amount = IArbV1SwapWrap(path[i]).swap(path[i+1], token0, path[i+2], _amount, _amount);
            token0 = path[i+2];
        }

        // Payback
        { 
            uint totalDebt = _amount.add(_fee);
            transferFundsBackToPoolInternal(_reserve, totalDebt);
            // profit = swapped_amount - _amount
        }        
    }
    // Lender is currently hard coded to Aaave
    function arbitrage( address lender, address loanAsset,  uint256 amount,  address[] memory path) external {
        
        bytes memory data = abi.encode(path);

        // Request loan
        ILendingPool lendingPool = ILendingPool(addressesProvider.getLendingPool());
        lendingPool.flashLoan(address(this), loanAsset, amount, data);
    }
}