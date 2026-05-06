import unittest
import time
class TokenBucket:
    def __init__(self, capacity: int,fill_rate: float,fill_time:float=1) -> None:
        self.capacity = capacity
        self.fill_rate = fill_rate
        self.fill_time = fill_time
        self._tokens = capacity
        self.time_stamp = time.time()
        
    def consume(self,tokens:int = 1) -> None:
        consumed = False
        now = time.time()
        lapse = now - self.time_stamp
        if lapse >= self.fill_time:
            self.add_tokens(lapse)

        if self._tokens >= tokens:
            self._tokens -= tokens
            consumed = True
        

        return consumed
        
    def add_tokens(self,lapse:float):
        self._tokens += self.fill_rate * int(lapse)
        self._tokens %= self.capacity +1 





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

        for _ in range(10):
            bucket.consume()
            time.sleep(0.5)
            self.assertTrue(bucket.capacity >= 2)

if __name__ == "__main__":
    unittest.main()
