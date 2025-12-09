"""Evaluation modules for LLM-as-a-judge"""
from .judge import LLMJudge
from .test_queries import TestSuite

__all__ = ['LLMJudge', 'TestSuite']
