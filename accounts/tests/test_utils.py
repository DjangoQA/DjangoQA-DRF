from unittest import TestCase

from accounts.utils import RedisConnection


class RedisConnectionTest(TestCase):
    def setUp(self):
        self.redis_instance = RedisConnection()

    def test_redis_is_exists_is_valid_otp_code(self):
        otp_code = self.redis_instance.set_otp('test_key')
        is_exists, is_valid = self.redis_instance.verify_otp('test_key', otp_code)
        self.assertTrue(is_exists)
        self.assertTrue(is_valid)

    def test_redis_is_exists_invalid_otp_code(self):
        self.redis_instance.set_otp('test_key')
        is_exists, is_valid = self.redis_instance.verify_otp('test_key', 'bad value')
        self.assertTrue(is_exists)
        self.assertFalse(is_valid)

    def test_redis_dont_exists_invalid_otp_code(self):
        is_exists, is_valid = self.redis_instance.verify_otp('no_exists_test_key', 'bad value')
        self.assertFalse(is_exists)
        self.assertFalse(is_valid)
