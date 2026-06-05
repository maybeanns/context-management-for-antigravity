from typing import Dict, Any, Callable
from harness import HarnessSession

class SimulatedAgent:
    def __init__(self, behavior_type: str = "success"):
        self.behavior_type = behavior_type
        self.loop_counter = 0

    def run_turn(self, session: HarnessSession, file_content: str, approval_callback: Callable[[], bool]) -> str:
        session.increment_turn()
        session.consume_budget(1000) # Mock token usage per turn

        if self.behavior_type == "success":
            session.log_turn("agent_thought", "Tying to edit the file to fix a syntax bug.")
            new_content = file_content + "\n# Fixed syntax error"
            session.verify_novelty(new_content)
            session.request_approval("write_file", approval_callback)
            session.log_turn("tool_call", {"tool": "write_file", "content": new_content})
            return new_content

        elif self.behavior_type == "stalling":
            # Infinite loop behavior: oscillates between two states
            session.log_turn("agent_thought", "Trying alternate fix.")
            self.loop_counter += 1
            if self.loop_counter % 2 == 0:
                new_content = file_content + "\n# Attempt A"
            else:
                new_content = file_content + "\n# Attempt B"
            
            # Since it oscillates, it will trigger the novelty check on the 3rd turn
            session.verify_novelty(new_content)
            session.request_approval("write_file", approval_callback)
            return new_content

        elif self.behavior_type == "high_token":
            # Consumes heavy tokens per turn
            session.consume_budget(50000)
            return file_content

        else:
            raise ValueError(f"Unknown behavior type: {self.behavior_type}")
