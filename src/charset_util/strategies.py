from abc import ABC, abstractmethod
from typing import Any, List, Optional
import json
import re

class RecoveryStrategy(ABC):
    @abstractmethod
    def apply(self, content: str) -> Optional[Any]:
        """
        Attempt to recover data from content.
        Returns the parsed data if successful, None otherwise.
        """
        pass

class DirectLoadStrategy(RecoveryStrategy):
    def apply(self, content: str) -> Optional[Any]:
        try:
            return json.loads(content)
        except:
            return None

class UnescapeQuotesStrategy(RecoveryStrategy):
    def apply(self, content: str) -> Optional[Any]:
        try:
            return json.loads(content.replace('\\"', '"'))
        except:
            return None

class BalanceBracesStrategy(RecoveryStrategy):
    def apply(self, content: str) -> Optional[Any]:
        balanced = self._balance_json(content)
        try:
            return json.loads(balanced)
        except:
            return None

    def _balance_json(self, json_str: str) -> str:
        if json_str.count('"') % 2 != 0:
            json_str += '"'
        
        stack = []
        for char in json_str:
            if char == '{':
                stack.append('}')
            elif char == '[':
                stack.append(']')
            elif char == '}' or char == ']':
                if stack and stack[-1] == char:
                    stack.pop()
        
        while stack:
            json_str += stack.pop()
            
        return json_str

class BalancedUnescapedStrategy(BalanceBracesStrategy):
    def apply(self, content: str) -> Optional[Any]:
        unescaped = content.replace('\\"', '"')
        return super().apply(unescaped)

class JsonRecoveryPipeline:
    def __init__(self, strategies: List[RecoveryStrategy] = None):
        self.strategies = strategies or [
            DirectLoadStrategy(),
            UnescapeQuotesStrategy(),
            BalanceBracesStrategy(),
            BalancedUnescapedStrategy()
        ]

    def process(self, content: str) -> Any:
        # Pre-processing: Extract likely JSON part
        candidate = self._extract_json_candidate(content)
        if not candidate:
            raise ValueError("No JSON-like structure found")

        last_error = None
        for strategy in self.strategies:
            result = strategy.apply(candidate)
            if result is not None:
                return result
        
        raise ValueError("All recovery strategies failed")

    def _extract_json_candidate(self, text: str) -> Optional[str]:
        match = re.search(r'[\{\[]', text)
        if match:
            return text[match.start():]
        return None
