import os
import sys
import tempfile
import pytest

# Add parent directory to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from harness import HarnessSession, BudgetExceededException, StallDetectedException, HumanRejectedException
from agent import SimulatedAgent

def test_harness_success():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "session.jsonl")
        session = HarnessSession(token_limit=10000, max_turns=5, log_path=log_file)
        agent = SimulatedAgent("success")
        
        initial_content = "def hello():\n  pass"
        
        # Turn 1
        content_after = agent.run_turn(session, initial_content, lambda: True)
        assert "# Fixed syntax error" in content_after
        assert session.turn_count == 1
        assert session.tokens_used == 1000

def test_harness_token_budget_exceeded():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "session.jsonl")
        # Set limit lower than agent consumption
        session = HarnessSession(token_limit=5000, max_turns=5, log_path=log_file)
        agent = SimulatedAgent("high_token")
        
        with pytest.raises(BudgetExceededException):
            agent.run_turn(session, "code", lambda: True)

def test_harness_turn_budget_exceeded():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "session.jsonl")
        session = HarnessSession(token_limit=100000, max_turns=2, log_path=log_file)
        agent = SimulatedAgent("success")
        
        initial_content = "code"
        c = agent.run_turn(session, initial_content, lambda: True)
        c = agent.run_turn(session, c, lambda: True)
        
        with pytest.raises(BudgetExceededException):
            agent.run_turn(session, c, lambda: True)

def test_harness_stall_detected():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "session.jsonl")
        session = HarnessSession(token_limit=100000, max_turns=10, log_path=log_file)
        agent = SimulatedAgent("stalling")
        
        initial_content = "code"
        # Oscillation edits:
        # Turn 1: code -> code + Attempt B
        # Turn 2: code + Attempt B -> code + Attempt B + Attempt A
        # Turn 3: code + Attempt B + Attempt A -> code + Attempt B + Attempt A + Attempt B (Wait, we append to previous content)
        # To test oscillation where content returns to a previous state:
        c1 = agent.run_turn(session, initial_content, lambda: True)
        c2 = agent.run_turn(session, c1, lambda: True)
        
        # On third turn, simulated agent will produce something that triggers verify_novelty
        with pytest.raises(StallDetectedException):
            # Manually feeding the same content to simulate stall:
            session.verify_novelty(c1)

def test_harness_human_rejection():
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "session.jsonl")
        session = HarnessSession(token_limit=10000, max_turns=5, log_path=log_file)
        agent = SimulatedAgent("success")
        
        with pytest.raises(HumanRejectedException):
            # Approval callback returns False
            agent.run_turn(session, "code", lambda: False)
