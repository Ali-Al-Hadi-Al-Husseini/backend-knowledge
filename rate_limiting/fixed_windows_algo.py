import unittest
import time

class FixedWindow:
    def __init__(self,limit:int=1,window_size:float=1):
        self.limit = limit
        self.window_size = window_size
        self.time_stamp = time.time()
        self.req_count = 0
    

    def allow_request(self):
        now = time.time()
        lapse = now -self.time_stamp
        if lapse >= self.window_size:
            self.time_stamp = now
            self.req_count = 0

        if self.req_count < self.limit:
            self.req_count += 1
            return True
        return False


class TestFixedWindow(unittest.TestCase):
    def setUp(self):
        self.limit = 3
        self.window_size = 1
        self.limiter = FixedWindow(limit=self.limit, window_size=self.window_size)

    def test_allow_within_limit(self):
        for i in range(self.limit):
            try:
                self.assertTrue(self.limiter.allow_request())
            except:
                print(self.limiter)

    def test_block_above_limit(self):
        for _ in range(self.limit):
            self.limiter.allow_request()
        self.assertFalse(self.limiter.allow_request())

    def test_window_reset(self):
        # Fill the current window
        for _ in range(self.limit):
            self.limiter.allow_request()
        self.assertFalse(self.limiter.allow_request())

        # Wait for the next window to start
        time.sleep(self.window_size + 0.1)
        
        # Should be able to send requests again
        self.assertTrue(self.limiter.allow_request())

    def test_multiple_windows(self):
        # Window 1
        for _ in range(self.limit):
            self.assertTrue(self.limiter.allow_request())
        
        time.sleep(self.window_size + 0.1)
        
        # Window 2
        for _ in range(self.limit):
            self.assertTrue(self.limiter.allow_request())

    def test_boundary_condition(self):
        # Testing if the counter resets exactly when it should
        bucket = FixedWindow(limit=1, window_size=0.5)
        self.assertTrue(bucket.allow_request())
        self.assertFalse(bucket.allow_request())
        
        time.sleep(0.6)
        self.assertTrue(bucket.allow_request())

if __name__ == "__main__":
    unittest.main()