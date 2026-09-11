from __future__ import annotations

import subprocess
import sys
import unittest
from unittest.mock import patch

import occ
import occ.free_surface as free_surface
import occ.parameterized as parameterized


MECHANICS_REQUEST = {
    "objects": ["rotating_frame", "steady_free_surface"],
    "observable": "signed_surface_height_difference",
    "parameters": {
        "angular_speed_rad_s": 7.2921159e-5,
        "latitude_rad": 0.7853981633974483,
        "velocity_enu_m_s": [0.0, 2.0, 0.0],
        "cross_channel_enu": [1.0, 0.0, 0.0],
        "width_m": 100.0,
        "gravity_m_s2": 9.81,
    },
}


class ParameterizedFlowTests(unittest.TestCase):
    def test_selected_owner_is_admitted_and_solved_once(self) -> None:
        with (
            patch.object(free_surface, "admit", wraps=free_surface.admit) as admit,
            patch.object(free_surface, "solve", wraps=free_surface.solve) as solve,
        ):
            result = parameterized.compile_problem(MECHANICS_REQUEST)

        self.assertEqual(result.status, "solved")
        admit.assert_called_once()
        solve.assert_called_once()

    def test_known_observable_with_wrong_objects_stops_after_admission(self) -> None:
        request = dict(MECHANICS_REQUEST, objects=["unrelated"])
        with (
            patch.object(free_surface, "admit", wraps=free_surface.admit) as admit,
            patch.object(free_surface, "solve", wraps=free_surface.solve) as solve,
        ):
            result = parameterized.compile_problem(request)

        self.assertEqual(result.obstruction.code, "no_adapter")
        admit.assert_called_once()
        solve.assert_not_called()

    def test_direct_domain_import_does_not_load_other_domain_owners(self) -> None:
        probe = """
import sys
import occ.free_surface
for name in ('occ.zeeman', 'occ.harmonic_current', 'occ.phonon'):
    assert name not in sys.modules, name
"""
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_package_root_is_not_a_public_facade(self) -> None:
        self.assertFalse(hasattr(occ, "compile_problem"))
        self.assertFalse(hasattr(occ, "Certificate"))


if __name__ == "__main__":
    unittest.main()
