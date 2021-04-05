pragma solidity ^0.6.6;

import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/math/SafeMath.sol";
import "OpenZeppelin/openzeppelin-contracts@3.0.0/contracts/token/ERC20/IERC20.sol";
import '../../uniswap-v2/IUniswapV2Pair.sol';
import "./IArbV1SwapWrap.sol";

contract SwapWrapUniv2 is  IArbV1SwapWrap {

    constructor() public {
    }
    
    function swap(address pair, address token0In, address token1Out, uint256 _amountIn, uint256 _expectedOut) external override returns (uint256) {
        bytes memory data = "";
        address token0 = IUniswapV2Pair(pair).token0();
        //address token1 = IUniswapV2Pair(pair).token0();
        uint256 amount0Out = _amountIn;
        uint256 amount1Out = 0;
        if(token0 == token1Out) {
            amount0Out = 0;
            amount1Out = _amountIn;
        }
        IERC20(token0In).transfer(pair, _amountIn);
        IUniswapV2Pair(pair).swap(amount0Out, amount1Out, msg.sender, data);
        return IERC20(token1Out).balanceOf(msg.sender);
    }
}
