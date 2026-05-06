import unittest
import time

class SlidingWindow:
    def __init__(self,limit:int= 1,window_size:float= 1):
        self.limit = limit
        self.window_size = window_size
        self.time_stamp = time.time()
    def allow_request(self)-> bool:
        pass

class TestSlidingWindow(unittest.TestCase):
    def setUp(self):
        self.limit = 3
        self.window_size = 1.0
        self.limiter = SlidingWindow(limit=self.limit, window_size=self.window_size)

    def test_allow_within_limit(self):
        for _ in range(self.limit):
            self.assertTrue(self.limiter.allow_request())

    def test_reject_over_limit(self):
        for _ in range(self.limit):
            self.limiter.allow_request()
        self.assertFalse(self.limiter.allow_request())

    def test_sliding_behavior(self):
        # 1. Send requests at specific intervals
        self.assertTrue(self.limiter.allow_request()) # Time: 0.0
        time.sleep(0.4)
        self.assertTrue(self.limiter.allow_request()) # Time: 0.4
        time.sleep(0.4)
        self.assertTrue(self.limiter.allow_request()) # Time: 0.8
        
        # 2. At 0.8s, we have 3 requests in the window. 4th should fail.
        self.assertFalse(self.limiter.allow_request())
        
        # 3. Wait until the first request (from 0.0s) falls out of the 1s window
        time.sleep(0.3) # Total time is now ~1.1s
        # Only requests from 0.4s and 0.8s are left. Space for one more!
        self.assertTrue(self.limiter.allow_request())

    def test_clean_old_requests(self):
        # Ensure the internal log doesn't grow forever
        for _ in range(self.limit):
            self.limiter.allow_request()
        
        time.sleep(self.window_size + 0.1)
        self.limiter.allow_request()
        
        # If implemented correctly, the internal queue length should 
        # reflect only active requests, not the expired ones.
        self.assertEqual(len(self.limiter.history), 1)

    def test_rapid_burst(self):
        # Sliding window should handle instant bursts correctly
        results = [self.limiter.allow_request() for _ in range(self.limit + 2)]
        self.assertEqual(results.count(True), 3)
        self.assertEqual(results.count(False), 2)

if __name__ == "__main__":
    unittest.main()
