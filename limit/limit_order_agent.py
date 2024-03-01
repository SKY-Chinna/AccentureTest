from trading_framework.execution_client import ExecutionClient
from trading_framework.price_listener import PriceListener


class LimitOrderAgent(PriceListener):

    def __init__(self, execution_client: ExecutionClient) -> None:
        """

        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        super().__init__()
        self.execution_client = execution_client
        self.held_orders = []

    def on_price_tick(self, product_id: str, price: float):
        # see PriceListener protocol and readme file
        for order in self.held_orders:
            if order['product_id'] == product_id:
                if order['action'] == 'buy' and price <= order['limit']:
                    self.execution_client.buy(product_id, order['amount'])
                    print(self.execution_client.buy(product_id, order['amount']))
                elif order['action'] == 'sell' and price >= order['limit']:
                    self.execution_client.sell(product_id, order['amount'])
                    print(self.execution_client.sell(product_id, order['amount']))
                self.held_orders.remove(order)

    def add_order(self, action: str, product_id: str, amount: int, limit: float):
        """
        Adds a new order to the agent's list of held orders.

        :param action: The action of the order (buy or sell).
        :param product_id: The ID of the product.
        :param amount: The amount to buy or sell.
        :param limit: The limit price at which to execute the order.
        """
        self.held_orders.append({
            'action': action,
            'product_id': product_id,
            'amount': amount,
            'limit': limit
        })

    def buy_ibm_below_100(self, product_id: str, price: float):
        """
        Buys 1000 shares of IBM when the price drops below $100.

        :param product_id: The ID of the product.
        :param price: The current price of the product.
        """
        if product_id == 'IBM' and price < 100:
            self.execution_client.buy(product_id, amount=1000)
            print(self.execution_client.buy(product_id, amount=1000))

        # Execution Finished
