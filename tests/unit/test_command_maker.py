"""
    Created: 05.11.2022
     Author: Bohdan Korzhak
             Ukraine

    All 'cmd' in tests obtained from Command Analyzer, EPOS Studio 3.7

"""

import unittest
from epos4 import command_maker


class TestCommandMaker(unittest.TestCase):
    def setUp(self) -> None:
        node_id = 1
        self.cm = command_maker.Epos4CommandMaker(node_id)

    def test_get_controlword(self):
        cmd = b'\x90\x02\x60\x02\x01\x40\x60\x00\x96\xa7'
        self.assertEqual(self.cm.get_controlword(), cmd)

    def test_send_controlword(self):
        cmd = b'\x90\x02\x68\x04\x01\x40\x60\x00\x0f\x00\x00\x00\xb3\x07'
        self.assertEqual(self.cm.send_controlword(0x0f), cmd)

    def test_get_statusword(self):
        cmd = b'\x90\x02\x60\x02\x01\x41\x60\x00\x22\xd1'
        self.assertEqual(self.cm.get_statusword(), cmd)

    def test_get_operation_mode(self):
        cmd = b'\x90\x02\x60\x02\x01\x61\x60\x00\x6c\xe6'
        self.assertEqual(self.cm.get_operation_mode(), cmd)

    def test_set_operation_mode(self):
        cmd = b'\x90\x02\x68\x04\x01\x60\x60\x00\x01\x00\x00\x00\xda\x67'
        self.assertEqual(self.cm.set_operation_mode(0x01), cmd)

    def test_get_position_pofile_velocity(self):
        cmd = b'\x90\x02\x60\x02\x01\x81\x60\x00\x86\x62'
        self.assertEqual(self.cm.get_position_profile_velocity(), cmd)

    def test_get_position_pofile_acceleration(self):
        cmd = b'\x90\x02\x60\x02\x01\x83\x60\x00\xee\x8f'
        self.assertEqual(self.cm.get_position_profile_acceleration(), cmd)

    def test_get_position_pofile_deceleration(self):
        cmd = b'\x90\x02\x60\x02\x01\x84\x60\x00\xc3\xde'
        self.assertEqual(self.cm.get_position_profile_deceleration(), cmd)

    def test_set_position_pofile_velocity(self):
        cmd = b'\x90\x02\x68\x04\x01\x81\x60\x00\xE7\x03\x00\x00\x7d\xd9'
        self.assertEqual(self.cm.set_position_profile_velocity(0x3E7), cmd)

    def test_set_position_pofile_acceleration(self):
        cmd = b'\x90\x02\x68\x04\x01\x83\x60\x00\x10\x27\x00\x00\xa6\xcd'
        self.assertEqual(self.cm.set_position_profile_acceleration(0x2710), cmd)

    def test_set_position_pofile_deceleration(self):
        cmd = b'\x90\x02\x68\x04\x01\x84\x60\x00\x10\x27\x00\x00\xbe\x0a'
        self.assertEqual(self.cm.set_position_profile_deceleration(0x2710), cmd)

    def test_get_target_position(self):
        cmd = b'\x90\x02\x60\x02\x01\x7A\x60\x00\xd4\xe3'
        self.assertEqual(self.cm.get_target_position(), cmd)

    def test_move_to_position(self):
        cmd = b'\x90\x02\x68\x04\x01\x7A\x60\x00\xE8\x03\x00\x00\x6e\x6e'
        self.assertEqual(self.cm.move_to_position(0x3E8), cmd)


if __name__ == "__main__":
    unittest.main()
