import unittest
from unittest.mock import MagicMock
from limit.limit_order_agent import LimitOrderAgent
from trading_framework.execution_client import ExecutionClient


class MockExecutionClient(ExecutionClient):
    """
    Mock ExecutionClient class for testing purposes.
    """
    def buy(self, product_id: str, amount: int):
        "dasdd"
        return f"An {product_id} purchase the shares by {amount}"


    def sell(self, product_id: str, amount: int):
        return f"An {product_id} sell the shares by {amount}"  # Mock sell method



class LimitOrderAgentTest(unittest.TestCase):

    def test_on_price_tick_execute_order(self):
        # Create a mock execution client
        execution_client = MockExecutionClient()

        # Create a limit order agent instance
        limit_order_agent = LimitOrderAgent(execution_client)

        # Add a buy order for AAPL at $150
        limit_order_agent.add_order('buy', 'AAPL', 100, 150)
        # Add a Sell order for CTS at $150
        limit_order_agent.add_order('sell', 'CTS', 1000, 120)

        # Simulate a price tick for AAPL at $140
        limit_order_agent.on_price_tick('AAPL', 140)
        print("Held Orders:", limit_order_agent.held_orders)

        # Simulate a price tick for AAPL at $160
        limit_order_agent.on_price_tick('AAPL', 160)
        print("Held Orders:", limit_order_agent.held_orders)


        # Simulate a price tick for CTS at $100
        limit_order_agent.on_price_tick('CTS', 100)
        print("Held Orders:", limit_order_agent.held_orders)

        # Simulate a price tick for CTS at $160
        limit_order_agent.on_price_tick('CTS', 125)
        print("Held Orders:", limit_order_agent.held_orders)



    def test_buy_ibm_below_100(self):
        # Create a mock ExecutionClient
        execution_client = MockExecutionClient()

        # Create a LimitOrderAgent instance
        limit_order_agent = LimitOrderAgent(execution_client)

        # Test when the price of IBM drops below $100
        limit_order_agent.buy_ibm_below_100('IBM', 99.5)

        print(limit_order_agent.buy_ibm_below_100('IBM', 99.5))
        # Test when the price of IBM is above $100
        limit_order_agent.buy_ibm_below_100('IBM', 105)


if __name__ == '__main__':
    unittest.main()
