import unittest
from client3 import getDataPoint,getRatio
from unittest.mock import patch

class ClientTest(unittest.TestCase):
  def test_getDataPoint_calculatePrice(self):
    quotes = [
      {'top_ask': {'price': 121.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    """ ------------ Add the assertion below ------------ """
    stock_1, bid_price_1, ask_price_1, price_1 = getDataPoint(quotes[0])
    self.assertEqual(stock_1, 'ABC')
    self.assertEqual(bid_price_1, 120.48)
    self.assertEqual(ask_price_1, 121.2)
    self.assertEqual(price_1, 120.84)

    stock_2, bid_price_2, ask_price_2, price_2 = getDataPoint(quotes[1])
    self.assertEqual(stock_2, 'DEF')
    self.assertEqual(bid_price_2, 117.87)
    self.assertEqual(ask_price_2, 121.68)
    self.assertEqual(price_2, 119.775)

  def test_getDataPoint_calculatePriceBidGreaterThanAsk(self):
    quotes = [
      {'top_ask': {'price': 119.2, 'size': 36}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 120.48, 'size': 109}, 'id': '0.109974697771', 'stock': 'ABC'},
      {'top_ask': {'price': 121.68, 'size': 4}, 'timestamp': '2019-02-11 22:06:30.572453', 'top_bid': {'price': 117.87, 'size': 81}, 'id': '0.109974697771', 'stock': 'DEF'}
    ]
    """ ------------ Add the assertion below ------------ """
    stock_1, bid_price_1, ask_price_1, price_1 = getDataPoint(quotes[0])
    self.assertEqual(stock_1, 'ABC')
    self.assertEqual(bid_price_1, 120.48)
    self.assertEqual(ask_price_1, 119.2)
    self.assertEqual(price_1, 119.84)

    stock_2, bid_price_2, ask_price_2, price_2 = getDataPoint(quotes[1])
    self.assertEqual(stock_2, 'DEF')
    self.assertEqual(bid_price_2, 117.87)
    self.assertEqual(ask_price_2, 121.68)
    self.assertEqual(price_2, 119.775)

  """ ------------ Add more unit tests ------------ """
  def test_getRatio(self):
   # Test positive ratio
   ratio = getRatio(10, 5)
   self.assertEqual(ratio, 2)

   # Test negative ratio
   ratio = getRatio(-8, 2)
   self.assertEqual(ratio, -4)

   # Test zero numerator
   ratio = getRatio(0, 10)
   self.assertEqual(ratio, 0)

   # Test zero denominator
   ratio = getRatio(10, 0)
   self.assertIsNone(ratio)

   # Test floating-point division
   ratio = getRatio(7, 3)
   self.assertAlmostEqual(ratio, 2.3333333, places=7)

  def test_edge_case(self):
    # Test with very high prices
    quote = {
        'stock': 'XYZ',
        'top_bid': {'price': 1e9},
        'top_ask': {'price': 2e9}
    }
    stock, bid_price, ask_price, price = getDataPoint(quote)
    self.assertEqual(price, 1.5e9)

    # Test with very low sizes
    quote = {
        'stock': 'ABC',
        'top_bid': {'price': 120.48, 'size': 1},
        'top_ask': {'price': 119.2, 'size': 0}
    }
    stock, bid_price, ask_price, price = getDataPoint(quote)
    self.assertEqual(stock, 'ABC')
    self.assertEqual(bid_price, 120.48)
    self.assertEqual(ask_price, 119.2)
    self.assertEqual(price, 119.84)

  def test_negative_case(self):
    # Test with missing 'top_ask' key
    quote = {
        'stock': 'DEF',
        'top_bid': {'price': 117.87},
    }
    with self.assertRaises(KeyError):
        stock, bid_price, ask_price, price = getDataPoint(quote)

    # Test with invalid price data type
    quote = {
        'stock': 'XYZ',
        'top_bid': {'price': '12E0.48'},
        'top_ask': {'price': 119.2}
    }
    with self.assertRaises(ValueError):
        stock, bid_price, ask_price, price = getDataPoint(quote)

  
if __name__ == '__main__':
    unittest.main()
