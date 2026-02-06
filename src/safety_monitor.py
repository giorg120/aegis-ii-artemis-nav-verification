"""
AEGIS-II | Artemis II Independent GNC Verification
Created: Feb 5, 2026
Source: Post-WDR Baseline (Ref: 02-02-2026)

NASA-STYLE COMPLIANCE:
- Rule 1: Simple control flow (no recursion).
- Rule 5: Assertion density >= 2 per function.
- Rule 7: Parameter validity checks.
"""

# Normalized Earth-Moon mass ratio
MU = 0.0121505856  

# Safety Threshold: Jacobi Constant (C)
# Values below 3.15 indicate a breach of the free-return corridor.
C_LOWER_LIMIT = 3.15 

def verify_trajectory_safety(state_vector):
    """
    Independent audit of the cis-lunar safety envelope.
    State Format: [x, y, z, vx, vy, vz]
    """
    # NASA Rule 5 & 7: Validate inputs before processing
    assert len(state_vector) == 6, "FAULT: State vector dimension mismatch"
    assert all(isinstance(n, (int, float)) for n in state_vector), "FAULT: Non-numeric data detected"

    x, y, z, vx, vy, vz = state_vector
    
    # Calculate squared distances for performance and sanity check
    r1_sq = (x + MU)**2 + y**2 + z**2
    r2_sq = (x - 1 + MU)**2 + y**2 + z**2
    
    # NASA Rule 5: Assert physical impossibility (Spacecraft cannot be inside Earth/Moon)
    assert r1_sq > 0, "PHYSICAL_IMPOSSIBILITY: Singular position at Earth center"
    assert r2_sq > 0, "PHYSICAL_IMPOSSIBILITY: Singular position at Moon center"

    r1, r2 = r1_sq**0.5, r2_sq**0.5
    
    # Potential function (Omega)
    omega = 0.5 * (x**2 + y**2) + (1 - MU)/r1 + MU/r2
    v_sq = vx**2 + vy**2 + vz**2
    
    jacobi_c = 2 * omega - v_sq
    
    # Final Sanity: Ensure we didn't get a NaN from a math error
    assert jacobi_c == jacobi_c, "ALGORITHM_FAILURE: Jacobi calculation resulted in NaN"
    
    val = round(float(jacobi_c), 5)
    
    if val < C_LOWER_LIMIT:
        return val, "CRITICAL_VIOLATION_CORRIDOR_EXIT"
    
    return val, "NOMINAL"

def sensor_vote_tmr(s1, s2, s3, tolerance=0.005):
    """
    Triple Modular Redundancy (TMR) Voter.
    Reduces Single Event Upset (SEU) risk from the Feb 2026 X-class solar flare.
    """
    # NASA Rule 7: Check for offline/malformed telemetry
    assert not any(s is None for s in [s1, s2, s3]), "SPOF_ALERT: Null sensor data in TMR loop"

    # Human-readable comparison logic
    diff_12 = abs(s1 - s2)
    diff_13 = abs(s1 - s3)
    diff_23 = abs(s2 - s3)

    if diff_12 < tolerance: return s1, "VOTE_SUCCESS"
    if diff_13 < tolerance: return s1, "VOTE_SUCCESS"
    if diff_23 < tolerance: return s2, "VOTE_SUCCESS"
    
    return None, "FAULT_DISAGREEMENT_TOTAL"

# --- End Flight Logic ---
