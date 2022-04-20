import unittest

from pi_device import create_pi_device, Mode


class PiDeviceTestCase(unittest.TestCase):
    def test_create_pi_device(self):
        host = "localhost"
        for port in range(50000, 50002):
            for mode in Mode:
                with self.subTest(mode = mode, port = port):
                    try:
                        dev1 = create_pi_device(host, port, mode)
                        dev2 = create_pi_device(host, port, mode)
                        self.assertIs(dev1, dev2)
                    except ConnectionRefusedError as e:
                        pass
