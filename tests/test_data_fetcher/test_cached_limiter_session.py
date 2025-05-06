
import unittest

from monte_carlo_simulator.data_fetcher.market_data_fetcher import CachedLimiterSession

class TestCachedLimiterSession(unittest.TestCase):

    session = CachedLimiterSession.get_session()

    def test_cached_limiter_session_init_exception(self):
        with self.assertRaises(Exception):
            CachedLimiterSession(limiter=None, bucket_class=None, backend=None)

    def test_cached_limiter_session_init_exception_message(self):
        try: 
            CachedLimiterSession(limiter=None, bucket_class=None, backend=None)
        except Exception as e:
            self.assertEqual(str(e), 'This is a Singleton class. Use get_session() to retrieve an instance instead.')
                               
    def test_cached_limiter_session_singleton(self):
        session_two = CachedLimiterSession.get_session()
        self.assertIs(self.session, session_two)

    def test_get_session_return_type(self):
        self.assertIsInstance(self.session, CachedLimiterSession)


if __name__ == '__main__':
    unittest.main()
