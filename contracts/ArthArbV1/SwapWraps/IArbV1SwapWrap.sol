pragma solidity ^0.6.6;

interface IArbV1SwapWrap {
    event Swap(
        address indexed sender,
        address token0, 
        address token1, 
        uint amount0Out, 
        uint amount1Out,
        uint amountOut
    );

    function swap(address pool, address token0, address token1, uint256 amount0In, uint256 amount1ExpOut) external returns (uint256 amountOut);
}