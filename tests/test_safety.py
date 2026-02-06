"""
AEGIS-II | System Verification Test Suite
Purpose: Stress-test the Safety Monitor against simulated sensor failure.
"""
from src.safety_monitor import verify_trajectory_safety, sensor_vote_tmr

def test_radiation_seu_mitigation():
    """Simulates a bit-flip from the X8.1 flare. S3 is faulted."""
    s1, s2, s3 = 1.012, 1.012, 0.0 
    val, status = sensor_vote_tmr(s1, s2, s3)
    assert val == 1.012, "FAULT: TMR failed to isolate bit-flip"
    assert status == "VOTE_SUCCESS"
    print("VERIFICATION PASSED: Radiation SEU isolated via TMR.")

def test_corridor_breach():
    """Simulates a spacecraft exceeding the energy limits."""
    danger_state = [1.0, 0.0, 0.0, 5.0, 5.0, 5.0] 
    val, status = verify_trajectory_safety(danger_state)
    assert status == "CRITICAL_VIOLATION_CORRIDOR_EXIT"
    print(f"VERIFICATION PASSED: Safety Alarm triggered at C = {val}")

if __name__ == "__main__":
    print("--- STARTING AEGIS-II SYSTEM AUDIT ---")
    test_radiation_seu_mitigation()
    test_corridor_breach()
    print("--- ALL SAFETY TESTS NOMINAL ---")
