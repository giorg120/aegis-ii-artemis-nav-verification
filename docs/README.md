---

##  NASA Flight Software Compliance (NPR 7150.2)
This project is architected according to the **NASA Power of 10** rules for safety-critical code:

- [x] **Rule 1 (Simple Control Flow):** No recursion or complex branching used in trajectory logic.
- [x] **Rule 2 (Fixed Bounds):** All loops and data structures have fixed, deterministic limits.
- [x] **Rule 3 (No Dynamic Memory):** Zero use of dynamic memory allocation to prevent heap fragmentation during the 10-day mission.
- [x] **Rule 5 (Assertion Density):** Minimum of 2 assertions per function to catch anomalous states (e.g., singular positions or NaNs).
- [x] **Rule 7 (Parameter Validation):** All telemetry inputs are validated for type and range before processing.

### 🛡️ Mission Assurance Strategy
During the simulated **February 2026 X8.1 Solar Flare**, the system utilizes **Triple Modular Redundancy (TMR)**. This ensures that even if radiation causes a bit-flip in one sensor's memory, the majority-voting logic maintains the integrity of the GNC (Guidance, Navigation, and Control) solution.
