#!/usr/bin/python3
import unittest
from console import HBNBCommand
from models.state import State
from models import storage


class TestHBNBCommand(unittest.TestCase):
    """ Tests for the HBNB console """

    def test_create_with_parameters(self):
        """Test create command with parameters"""
        cmd = HBNBCommand()
        cmd.onecmd('create State name="California"')
        state_objs = storage.all(State)
        self.assertEqual(len(state_objs), 1)
        for state in state_objs.values():
            self.assertEqual(state.name, "California")


if __name__ == "__main__":
    unittest.main()
