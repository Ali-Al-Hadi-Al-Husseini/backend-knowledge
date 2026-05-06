from collections import deque
import time

class LeakyBucket:
    def __init__(self,capacity=1,leak_rate:float= 1,leak_time:float= 1):
        self.queue = deque()
        self.capacity =  capacity
        self.leak_rate = leak_rate
        self.leak_time = leak_time
        self.time_stamp = time.time()
        
    def add_request(self):
        now = time.time() 
        lapse = now - self.time_stamp
        added = False

        if lapse >= self.leak_time:
            self.leak(now)
        if len(self.queue) < self.capacity:
            self.queue.append("req")
            added = True
        return added

        

    def leak(self,now:float):
        for _ in range(int(self.leak_rate)):
            if self.queue:
                self.queue.popleft()
        self.time_stamp = now






import unittest

class TestLeakyBucket(unittest.TestCase):
    def setUp(self):
        self.capacity = 5
        self.leak_rate = 2 
        self.bucket = LeakyBucket(capacity=self.capacity, leak_rate=self.leak_rate)

    def test_add_to_empty_bucket(self):
        for i in range(self.capacity):
            self.assertTrue(self.bucket.add_request())

    def test_overflow(self):
        for _ in range(self.capacity):
            self.bucket.add_request()
        self.assertFalse(self.bucket.add_request())

    def test_leak_behavior(self):
        bucket = LeakyBucket(capacity=1, leak_rate=10,leak_time=0.1)
        self.assertTrue(bucket.add_request())
        self.assertFalse(bucket.add_request())
        time.sleep(0.15)
        self.assertTrue(bucket.add_request())

    def test_burst_handling(self):
        bucket = LeakyBucket(capacity=10, leak_rate=1)
        results = [bucket.add_request() for _ in range(10)]
        self.assertTrue(all(results))
        self.assertFalse(bucket.add_request())

    def test_partial_leak(self):
        bucket = LeakyBucket(capacity=5, leak_rate=1)
        for _ in range(5):
            bucket.add_request()
        time.sleep(0.5) 
        self.assertFalse(bucket.add_request())
        time.sleep(0.6)
        self.assertTrue(bucket.add_request())

if __name__ == "__main__":
    unittest.main()