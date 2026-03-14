Topic 2 — Preparing for Test Automation (Chapter 2)
TAE-2.1.1 — Infrastructure Configuration for Test Automation

1. Concept Explanation
Before a single test script can run, the infrastructure must be ready to support automation. This sounds obvious but it is the most commonly skipped step in automation projects — teams jump straight to writing scripts without asking whether the SUT is actually automatable.
The syllabus defines three core requirements for a testable SUT:
Observability — the SUT must expose interfaces that let the automation see what is happening inside it. Without observability, your test cannot determine whether the actual result matches the expected result. In a web application this means DOM elements with stable IDs. In an ECU this means diagnostic interfaces, CAN signal outputs, or memory read access.
Controllability — the SUT must expose interfaces that let the automation drive it. Without controllability, your test cannot stimulate the SUT into the state you need to test. In a web application this means clickable elements and form inputs. In an ECU this means CAN message injection, fault simulation interfaces, or calibration parameter access.
Architecture transparency — the documentation must clearly describe what interfaces exist at each test level, where they are, and how to use them. Without this, the TAE cannot design automation that actually reaches the right layer.
Why this concept exists: Automation fails not because the scripts are wrong but because the SUT was never designed to be automatable. Testability is a non-functional requirement — exactly like performance or security — and must be designed in from the beginning, not retrofitted later.
When it should NOT be assumed: Never assume testability exists just because the SUT has been manually tested. Manual testers use human judgment to work around missing interfaces. Automation cannot. A manual tester can look at a screen and say "that looks wrong." An automated test needs a machine-readable signal to make the same determination.
Common misunderstanding: Many teams treat testability as a testing team problem. It is not. It is a system design problem. The software architect owns testability as a non-functional requirement. The TAE's role is to identify the specific gaps and communicate them to the architect early — ideally during the design phase, not after the system is built.

2. Real Industry Implementation
In mature organizations, testability requirements are written into the system architecture specification alongside performance and security requirements. A TAE is involved in architecture reviews specifically to evaluate whether the proposed design supports the required test levels.
Practical mechanisms used:
Accessibility identifiers — in UI systems, every interactive element gets a stable, unique ID assigned either automatically by the framework or manually by developers. This is the single most impactful testability improvement for UI automation. Without it, automation relies on fragile XPath expressions that break on every UI change.
System environment variables — application behavior parameters that can be changed through configuration to enable testing modes. For example, disabling authentication in a test environment, enabling verbose logging, or switching to a mock payment gateway. These give the TAF controllability over application state without requiring UI interaction.
Deployment variables — similar to environment variables but set at deployment time rather than runtime. In containerized systems these are injected as environment variables in the deployment manifest. In automotive ECU systems these are calibration parameters loaded before test execution.
Architecture pattern — testability layer:
