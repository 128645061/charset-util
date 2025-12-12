from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple
import json
import re
import logging
import html

logger = logging.getLogger(__name__)

class RecoveryStrategy(ABC):
    """
    Abstract base class for all JSON recovery strategies.
    定义所有JSON修复策略的抽象基类。
    """
    @abstractmethod
    def apply(self, content: str) -> Optional[Any]:
        """
        Attempt to recover data from content.
        尝试从内容中恢复数据。
        
        Args:
            content: The string content to parse (字符串内容)
            
        Returns:
            The parsed data if successful, None otherwise. (成功返回解析后的数据，失败返回None)
        """
        pass
    
    def apply_with_suffix(self, content: str) -> Tuple[Optional[Any], str]:
        """
        Attempt to recover data and return the unused suffix.
        尝试恢复数据并返回未使用的后缀。
        
        Args:
            content: The string content to parse
            
        Returns:
            Tuple of (parsed_data, suffix).
            If parsing failed, parsed_data is None.
            Default implementation returns empty suffix if successful.
        """
        result = self.apply(content)
        return result, ""

class DirectLoadStrategy(RecoveryStrategy):
    """
    Strategy 1: Direct Load
    策略1：直接加载
    
    Attempts to parse the content as valid JSON. This is the baseline check.
    尝试直接将内容解析为合法的JSON。这是最基本的检查。
    """
    def apply(self, content: str) -> Optional[Any]:
        try:
            return json.loads(content)
        except:
            return None

class UnescapeQuotesStrategy(RecoveryStrategy):
    """
    Strategy 2: Unescape Quotes
    策略2：去除转义引号
    
    Handles cases where JSON is embedded inside a string and quotes are escaped.
    e.g. "{\"key\": \"value\"}" -> {"key": "value"}
    处理JSON嵌套在字符串中且引号被转义的情况。
    """
    def apply(self, content: str) -> Optional[Any]:
        try:
            return json.loads(content.replace('\\"', '"'))
        except:
            return None

class BalanceBracesStrategy(RecoveryStrategy):
    """
    Strategy 3: Balance Braces
    策略3：平衡括号
    
    Handles truncated JSON by heuristically appending missing closing braces/brackets.
    e.g. {"key": "value" -> {"key": "value"}
    处理被截断的JSON，通过启发式算法自动补全缺失的右括号/右中括号。
    """
    def apply(self, content: str) -> Optional[Any]:
        balanced = self._balance_json(content)
        try:
            return json.loads(balanced)
        except:
            return None

    def _balance_json(self, json_str: str) -> str:
        # If quotes are unbalanced (odd number), append a closing quote first
        # 如果引号数量是奇数，说明字符串也被截断了，先补一个引号
        if json_str.count('"') % 2 != 0:
            json_str += '"'
        
        # Use a stack to track opening braces/brackets
        # 使用栈来跟踪左括号
        stack = []
        for char in json_str:
            if char == '{':
                stack.append('}')
            elif char == '[':
                stack.append(']')
            elif char == '}' or char == ']':
                # If we encounter a closing brace, match it with the stack top
                # 如果遇到右括号，尝试与栈顶匹配
                if stack and stack[-1] == char:
                    stack.pop()
        
        # Append all missing closing braces in reverse order (LIFO)
        # 逆序补全所有缺失的右括号
        while stack:
            json_str += stack.pop()
            
        return json_str

class BalancedUnescapedStrategy(BalanceBracesStrategy):
    """
    Strategy 4: Balanced & Unescaped
    策略4：平衡且去除转义
    
    Combines unescaping quotes and balancing braces. Useful for truncated JSON strings inside other strings.
    结合了去除转义和平衡括号。适用于嵌套在其他字符串中且被截断的JSON。
    """
    def apply(self, content: str) -> Optional[Any]:
        unescaped = content.replace('\\"', '"')
        return super().apply(unescaped)

class PartialTruncationStrategy(BalancedUnescapedStrategy):
    """
    Strategy 5: Partial Truncation Repair
    策略5：局部截断修复
    
    Handles cases where truncation happens inside a string or escape sequence.
    e.g. {"msg": "Hello Wor -> {"msg": "Hello Wor"}
    e.g. {"msg": "Hello \\u4f -> {"msg": "Hello "} (Trims incomplete escape)
    处理截断发生在字符串内部或转义序列中间的情况。
    
    Inherits from BalancedUnescapedStrategy to handle escaped quotes as well.
    继承自 BalancedUnescapedStrategy 以同时处理转义引号。
    """
    def _trim(self, content: str) -> str:
        """Helper to trim trailing incomplete sequences."""
        while True:
            content = content.rstrip()
            original_len = len(content)
            
            # 1. Trim incomplete escape sequences at the end
            # Matches backslash at the very end
            if content.endswith('\\'):
                logger.debug("PartialTruncationStrategy: Trimming trailing backslash")
                content = content[:-1]
                continue
            
            # 1b. Trim incomplete unicode escape
            # Matches \u followed by 0-3 hex digits at the end
            # e.g. "abc\u4" -> "abc"
            match = re.search(r'(\\u[0-9a-fA-F]{0,3})$', content)
            if match:
                 logger.debug("PartialTruncationStrategy: Trimming incomplete unicode escape")
                 content = content[:match.start()]
                 continue

            # 2. If ends with comma, remove it
            if content.endswith(','):
                logger.debug("PartialTruncationStrategy: Trimming trailing comma")
                content = content[:-1]
                continue
            
            # 3. If ends with quote (or escaped quote), check if it's an OPENING quote
            # Heuristic: It's an opening quote if it follows a comma, {, or [
            if content.endswith('"'):
                # Check what comes before the quote
                # Handle escaped quote \"
                quote_len = 1
                if content.endswith('\\"'):
                    quote_len = 2
                
                # Look behind
                pre_quote = content[:-quote_len].rstrip()
                # logger.debug(f"Pre-quote end: {repr(pre_quote[-10:])}")
                
                if pre_quote and (pre_quote.endswith(',') or pre_quote.endswith('{') or pre_quote.endswith('[')):
                    logger.debug(f"PartialTruncationStrategy: Trimming trailing quote (len={quote_len})")
                    content = content[:-quote_len]
                    continue

            # 4. Trim garbage suffix (e.g. "(truncated)", "...", etc.)
            # JSON never ends with ')', '.', '>'
            if content.endswith(')'):
                last_open = content.rfind('(')
                if last_open != -1:
                    logger.debug("PartialTruncationStrategy: Trimming parenthesized suffix")
                    content = content[:last_open]
                    continue
            
            if content.endswith('.'):
                logger.debug("PartialTruncationStrategy: Trimming trailing dot")
                content = content[:-1]
                continue

            if content.endswith('>'):
                last_open = content.rfind('<')
                if last_open != -1:
                    logger.debug("PartialTruncationStrategy: Trimming <...> suffix")
                    content = content[:last_open]
                    continue
            
            if len(content) == original_len:
                break
        return content

    def apply(self, content: str) -> Optional[Any]:
        trimmed = self._trim(content)
        return super().apply(trimmed)

    def apply_with_suffix(self, content: str) -> Tuple[Optional[Any], str]:
        trimmed = self._trim(content)
        suffix = content[len(trimmed):]
        # Since super() is BalancedUnescapedStrategy which doesn't implement apply_with_suffix 
        # (it uses default which returns empty string suffix), we just use super().apply()
        result = super().apply(trimmed)
        return result, suffix

class HTMLUnescapeStrategy(RecoveryStrategy):
    """
    Strategy 6: HTML Unescape
    策略6：HTML实体反转义
    
    Handles JSON containing HTML entities (e.g. &quot; instead of ").
    处理包含HTML实体的JSON。
    """
    def apply(self, content: str) -> Optional[Any]:
        try:
            unescaped = html.unescape(content)
            # After unescaping, it might be a valid JSON or need balancing
            # Try direct load first
            try:
                return json.loads(unescaped)
            except:
                # If failed, try balancing it (reusing logic from BalanceBracesStrategy)
                # We instantiate BalanceBracesStrategy here or just duplicate logic?
                # Let's use composition.
                balancer = BalanceBracesStrategy()
                return balancer.apply(unescaped)
        except:
            return None

class JsonRecoveryPipeline:
    """
    The main pipeline that orchestrates multiple recovery strategies.
    协调多种修复策略的主流水线。
    """
    def __init__(self, strategies: List[RecoveryStrategy] = None):
        # Default order of strategies: from strictest to most heuristic
        # 默认策略顺序：从最严格（最快）到最启发式（最慢/最宽容）
        self.strategies = strategies or [
            DirectLoadStrategy(),
            UnescapeQuotesStrategy(),
            BalanceBracesStrategy(),
            BalancedUnescapedStrategy(),
            PartialTruncationStrategy(),
            HTMLUnescapeStrategy()
        ]

    def process(self, content: str) -> Any:
        """
        Run the content through the pipeline strategies until one succeeds.
        将内容通过流水线策略运行，直到有一个成功为止。
        """
        # Pre-processing: Extract likely JSON part (find first '{' or '[')
        # 预处理：提取可能的JSON部分（寻找第一个 '{' 或 '['）
        candidate = self._extract_json_candidate(content)
        if not candidate:
            logger.debug("No JSON-like structure found in content")
            raise ValueError("No JSON-like structure found")

        for strategy in self.strategies:
            strategy_name = strategy.__class__.__name__
            logger.debug(f"Attempting strategy: {strategy_name}")
            result = strategy.apply(candidate)
            if result is not None:
                logger.info(f"Successfully recovered JSON using strategy: {strategy_name}")
                return result
            logger.debug(f"Strategy {strategy_name} failed")
        
        logger.error("All recovery strategies failed")
        raise ValueError("All recovery strategies failed")
    
    def process_with_suffix(self, content: str) -> Tuple[Any, str]:
        """
        Run the content through the pipeline strategies until one succeeds, returning data and unused suffix.
        将内容通过流水线策略运行，直到有一个成功为止，返回数据和未使用的后缀。
        """
        candidate = self._extract_json_candidate(content)
        if not candidate:
            logger.debug("No JSON-like structure found in content")
            raise ValueError("No JSON-like structure found")
        
        # Calculate prefix skipped by _extract_json_candidate to adjust suffix later?
        # No, _extract_json_candidate returns a substring.
        # But wait, if _extract_json_candidate trims the START, the suffix is relative to THAT substring.
        # So we don't need to worry about the prefix here, as extract_and_recover handles the main prefix.
        # But if process_with_suffix is called on "abc{...}xyz", candidate is "{...}xyz".
        # If strategy uses "{...}", suffix is "xyz".
        
        for strategy in self.strategies:
            strategy_name = strategy.__class__.__name__
            logger.debug(f"Attempting strategy: {strategy_name}")
            result, suffix = strategy.apply_with_suffix(candidate)
            if result is not None:
                logger.info(f"Successfully recovered JSON using strategy: {strategy_name}")
                return result, suffix
            logger.debug(f"Strategy {strategy_name} failed")
            
        logger.error("All recovery strategies failed")
        raise ValueError("All recovery strategies failed")

    def _extract_json_candidate(self, text: str) -> Optional[str]:
        match = re.search(r'[\{\[]', text)
        if match:
            return text[match.start():]
        return None
