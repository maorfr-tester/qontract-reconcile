import os
import sys
from unittest import TestCase, skipIf
from unittest.mock import patch

from reconcile.utils import gpg


VALID_KEY = """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
W1DegErhvC6nwh/J0GOLws2gRzVo+2RzB7if"""


class TestGpgKeyValid(TestCase):
    def test_gpg_key_invalid_spaces(self):
        key = 'key with spaces'
        with self.assertRaises(ValueError) as e:
            gpg.gpg_key_valid(key)
        self.assertEqual(str(e.exception), gpg.ERR_SPACES)

    def test_gpg_key_invalid_equal_signs(self):
        key = 'equal=signs=not=at=end=of=key'
        with self.assertRaises(ValueError) as e:
            gpg.gpg_key_valid(key)
        self.assertEqual(str(e.exception), gpg.ERR_EQUAL_SIGNS)

    def test_gpg_key_invalid_base64(self):
        # $ echo -n "hello world" | base64
        # aGVsbG8gd29ybGQ=
        key = 'aGVsbG8gd29ybGQ'
        with self.assertRaises(ValueError) as e:
            gpg.gpg_key_valid(key)
        self.assertEqual(str(e.exception), gpg.ERR_BASE64)


# We have to mangle the namespace of the gpg module, since it imports
# Popen. Had that module chosen "import subprocess;
# subprocess.Popen(...)" we'd be patching subprocess instead.
class TestGpgEncrypt(TestCase):
    @patch.object(gpg, 'run')
    def test_gpg_encrypt_all_ok(self, popen):
        popen.return_value.stdout = b"<stdout>"

        self.assertEqual(gpg.gpg_encrypt('acontent', 'akey'),
                         '<stdout>')

    @skipIf((sys.version_info.major, sys.version_info.minor) == (3, 6) and
            os.getuid() == 0,
            "Jenkins and Python 3.6 fail this test")
    def test_gpg_encrypt_nomocks(self):
        self.assertTrue(
            gpg.gpg_encrypt("a message", VALID_KEY)
        )
