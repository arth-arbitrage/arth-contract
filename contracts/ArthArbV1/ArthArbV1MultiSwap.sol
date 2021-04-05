pragma solidity ^0.6.6;

// SPDX-License-Identifier: MIT

import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/math/SafeMath.sol";
import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/token/ERC20/SafeERC20.sol";

import "./SwapWraps/IArbV1SwapWrap.sol";
import '../ArthDexV1/IArthDexV1Pair.sol';

interface IArthLending {
  function flashLoan ( address _receiver, address _reserve, uint256 _amount, bytes calldata _params ) external;
}

interface IFlashLoanReceiver {
    function executeOperation(address _reserve, uint256 _amount, uint256 _fee, bytes calldata _params) external;
}

contract ArthArbV1MultiSwap is IFlashLoanReceiver {

    //using SafeERC20 for IERC20;
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    // Events
    event borrowMade(address _reserve, uint256 _amount , uint256 _fee);
    event tradeMade(uint256 _amount);
    event Received(address caller, uint amount, string message);
    
    constructor(address _registryAddressr) public {
        //_registryAddress // future use
    }

    address constant ethAddress = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

    function getBalanceInternal(address _target, address _reserve) internal view returns(uint256) {
        if(_reserve == ethAddress) {
            return _target.balance;
        }
        return IERC20(_reserve).balanceOf(_target);
    }

    function executeOperation(
        address _reserve,
        uint256 _amount,
        uint256 _fee,
        bytes calldata _params
    )
        external
        override
    {        
        emit borrowMade(_reserve,_amount, _fee);

        (address lender, address[] memory path, uint256[] memory  amounts) = abi.decode(_params, (address, address[], uint256[]));
        require(_amount == amounts[0]);
        require(path.length >= 3, 'ArthArbV1MultiSwap: INVALID_PATH');
        address token0 = _reserve;
        uint256 j = 1;
        uint256 amountIn = _amount;
        for (uint i = 0; i <  path.length; i=i+3) {
            address swapWrapp = path[i];
            address pool = path[i+1];
            address token1 = path[i+2];
            uint256 amountOut = amounts[j];
            (bool success, bytes memory returnData) = swapWrapp.delegatecall(abi.encodeWithSelector(IArbV1SwapWrap(swapWrapp).swap.selector,
                                    pool, token0, token1, amountIn, amountOut));
            j++;
            token0 = token1;
            amountIn = amountOut;
            assert(success);
        }

        if(_reserve == ethAddress) {
            (bool success, ) = lender.call{value: _amount}("");
            require(success == true, "Couldn't transfer ETH");
            return;
        } else {
            IERC20(_reserve).safeTransfer(lender, _amount);
        }     
    }    
    /**
     ** Flash loan amount (18 decimals) worth of `_asset`
     */
    function arbitrage(address lender, address loanAsset, address[] memory path, uint256[] memory amounts ) 
        external 
        //onlyOwner 
    {
        bytes memory data = abi.encode(lender, path, amounts);
        // Request loan
        IArthLending(lender).flashLoan(address(this), loanAsset, amounts[0], data);
    }

    /**
     ** Flash loan amount (18 decimals) worth of `_asset`
     */
    function exchange(address swapWrapp, address pool, address token0, address token1, uint256 amountIn, uint256  amountOut ) 
        external 
        //onlyOwner 
    {
        (bool success, bytes memory returnData) = swapWrapp.delegatecall(abi.encodeWithSelector(IArbV1SwapWrap(swapWrapp).swap.selector,
                                    pool, token0, token1, amountIn, amountOut));
        assert(success);
    }

    receive() external payable {
        emit Received(msg.sender, msg.value, "Fallback was called");
    }
}
