import unittest
import time
class TokenBucket:
    def __init__(self):
        pass
        
    def consume(self):
        pass






class TestTokenBucket(unittest.TestCase):
    def test_initial_capacity(self):
        bucket = TokenBucket(capacity=5, fill_rate=1)

        for _ in range(5):
            self.assertTrue(bucket.consume())

        self.assertFalse(bucket.consume())

    def test_refill_logic(self):

        bucket = TokenBucket(capacity=1, fill_rate=1)
        self.assertTrue(bucket.consume()) 
        self.assertFalse(bucket.consume()) 
        
        time.sleep(1.1) 
        self.assertTrue(bucket.consume()) 

    def test_capacity_limit(self):
        bucket = TokenBucket(capacity=2, fill_rate=10)
        time.sleep(0.5) 
        self.assertTrue(bucket.consume())
        self.assertTrue(bucket.consume())
        self.assertFalse(bucket.consume())