pragma solidity ^0.6.0;

// SPDX-License-Identifier: MIT

interface IArthDexV1Pair {

    event Swap(
        address indexed sender,
        uint amount0In,
        uint amount1In,
        uint amount0Out,
        uint amount1Out,
        address indexed to
    );
    event Sync(uint112 reserve0, uint112 reserve1);

    function MINIMUM_LIQUIDITY() external pure returns (uint);
    function owner() external view returns (address);
    function token0() external view returns (address);
    function token1() external view returns (address);
    function getReserves() external view returns (uint112 reserve0, uint112 reserve1, uint32 blockTimestampLast);

    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external;
    function getAmountOut(uint amountIn, address _token0, address _token1) external view returns (uint amountOut);

    function skim(address to) external;
    function sync() external;

    function initialize(address, address) external;
     function setFee(uint256 _fee) external;
}
