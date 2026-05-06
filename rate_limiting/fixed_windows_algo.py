import unittest
import time

class TestFixedWindow(unittest.TestCase):
    def setUp(self):
        self.limit = 3
        self.window_size = 1
        self.limiter = FixedWindow(limit=self.limit, window_size=self.window_size)

    def test_allow_within_limit(self):
        for i in range(self.limit):
            self.assertTrue(self.limiter.allow_request())

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