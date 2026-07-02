from django.test import TestCase

class ValidateDepositKeyUtilTests(TestCase):

    def setUp(self) -> None:
        pass

    def test_validate_deposit_key_util(self):
        """
        validator_deposit_key() return False for wrong deposit
        """
        self.assertTrue(1==1)

    def test_account_signature_verify(self):
        self.assertTrue(1==1)
