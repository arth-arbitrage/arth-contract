pragma solidity ^0.6.6;

import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/math/SafeMath.sol";
import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/token/ERC20/IERC20.sol";
import '../../ArthDexV1/IArthDexV1Pair.sol';
import "./IArbV1SwapWrap.sol";

contract SwapWrapArthV1 is  IArbV1SwapWrap {

    constructor() public {
    }
    
    // _token1Out is not used, expectedOut is ignored
    function swap(address pair, address _token0, address _token1, uint256 _amountIn, uint256 _expectedOut) external override returns (uint256 amountOut) {
        bytes memory data = "";
        address token0 = IArthDexV1Pair(pair).token0();
        address token1 = IArthDexV1Pair(pair).token1();

        if(token0 == _token0 && token1 == _token1) {
            IERC20(token0).transfer(pair, _amountIn);
            IArthDexV1Pair(pair).swap(0, _expectedOut, address(this), data);
            amountOut = IERC20(token1).balanceOf(msg.sender);
        } else if(token0 == _token1 && token1 == _token0) {
            IERC20(token1).transfer(pair, _amountIn);
            IArthDexV1Pair(pair).swap(_expectedOut, 0, address(this), data);
            amountOut = IERC20(token0).balanceOf(msg.sender);
        } else {
            require(false, "Tokens not supported!");
        }
    }
}
