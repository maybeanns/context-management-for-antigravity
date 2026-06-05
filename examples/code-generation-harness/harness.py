import os
import json
import logging
from typing import Dict, List, Any, Callable

class HarnessException(Exception):
    pass

class BudgetExceededException(HarnessException):
    pass

class StallDetectedException(HarnessException):
    pass

class HumanRejectedException(HarnessException):
    pass

class HarnessSession:
    def __init__(self, token_limit: int, max_turns: int, log_path: str):
        self.token_limit = token_limit
        self.max_turns = max_turns
        self.log_path = log_path
        self.tokens_used = 0
        self.turn_count = 0
        self.history: List[Dict[str, Any]] = []
        self.edit_history: List[str] = []  # Stores SHA/hashes or contents of modified files to detect loop
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("HarnessSession")

    def log_turn(self, turn_type: str, content: Any):
        log_entry = {
            "turn": self.turn_count,
            "type": turn_type,
            "content": content
        }
        self.history.append(log_entry)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def consume_budget(self, tokens: int):
        self.tokens_used += tokens
        if self.tokens_used > self.token_limit:
            raise BudgetExceededException(f"Token budget of {self.token_limit} exceeded: used {self.tokens_used}")

    def increment_turn(self):
        self.turn_count += 1
        if self.turn_count > self.max_turns:
            raise BudgetExceededException(f"Turn count limit of {self.max_turns} exceeded.")

    def verify_novelty(self, file_content: str):
        """Detect stalls or repeating edit cycles."""
        # Simple novelty check: if the exact same file content has been produced before
        if file_content in self.edit_history:
            raise StallDetectedException("Stall detected: file content returned to a previously seen state.")
        self.edit_history.append(file_content)

    def request_approval(self, action: str, approval_callback: Callable[[], bool]) -> bool:
        """Enforces human-in-the-loop approval boundaries."""
        self.logger.info(f"Requesting approval for action: {action}")
        approved = approval_callback()
        if not approved:
            raise HumanRejectedException(f"Action rejected by user: {action}")
        return True
