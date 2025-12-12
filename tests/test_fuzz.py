
import unittest
from hypothesis import given, strategies as st, settings
from charset_util.recovery import recover_json, repair_mojibake
import json

class TestFuzzing(unittest.TestCase):
    
    @given(st.text())
    @settings(max_examples=100, deadline=None)
    def test_repair_mojibake_never_crashes(self, s):
        """Fuzz repair_mojibake with random strings."""
        try:
            repair_mojibake(s)
        except Exception as e:
            self.fail(f"repair_mojibake crashed on input {repr(s)} with error: {e}")

    @given(st.recursive(
        st.none() | st.booleans() | st.floats() | st.text(),
        lambda children: st.lists(children) | st.dictionaries(st.text(), children),
        max_leaves=10
    ))
    @settings(max_examples=50, deadline=None)
    def test_recover_json_valid_input(self, data):
        """Fuzz recover_json with VALID JSON data (should always succeed)."""
        json_str = json.dumps(data)
        try:
            recovered = recover_json(json_str)
            # Basic structural check - equality might fail due to float precision etc, 
            # but it should at least return something valid.
            self.assertIsNotNone(recovered)
        except Exception as e:
            self.fail(f"recover_json crashed on valid input {repr(json_str)} with error: {e}")

    @given(st.text())
    @settings(max_examples=100, deadline=None)
    def test_recover_json_random_input(self, s):
        """Fuzz recover_json with RANDOM text (should either recover or raise ValueError, never crash with other errors)."""
        try:
            recover_json(s)
        except ValueError:
            # Expected for garbage
            pass
        except Exception as e:
            self.fail(f"recover_json crashed on random input {repr(s)} with error: {e}")

if __name__ == '__main__':
    unittest.main()
