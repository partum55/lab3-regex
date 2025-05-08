"""Own ReGeX implementation"""

from abc import ABC, abstractmethod


class State(ABC):
    """Base class for a state in the regex FSM."""

    def __init__(self):
        self.next_states = []

    def add_next(self, state: "State"):
        """Add a transition to the given state."""
        self.next_states.append(state)

    @abstractmethod
    def check_self(self, char: str):
        """Return True if this state matches the given character."""
        pass

class StartState(State):
    """State representing the start of the regex pattern."""

    def check_self(self, char: str):
        """Start state never matches any character."""
        return False

class TerminationState(State):
    """State representing the successful end of the regex pattern."""

    def check_self(self, char: str):
        """Termination state never matches any character."""
        return False

class AsciiState(State):
    """State for matching a specific literal character."""

    def __init__(self, char: str):
        super().__init__()
        self.char = char

    def check_self(self, curr_char: str):
        """Return True if curr_char equals the expected symbol."""
        return curr_char == self.char

class DotState(State):
    """State for '.' which matches any single character."""

    def check_self(self, char: str):
        """Return True for any character match."""
        return True

class StarState(State):
    """Placeholder for '*' quantifier; matching logic in FSM."""

    def __init__(self):
        super().__init__()
        self.loop_state = None

    def check_self(self, char: str):
        """Star state does not consume characters directly."""
        return False

class PlusState(State):
    """Placeholder for '+' quantifier; matching logic in FSM."""

    def __init__(self):
        super().__init__()
        self.loop_state = None

    def check_self(self, char: str):
        """Plus state does not consume characters directly."""
        return False

class RegexFSM:
    """A simple regex engine supporting literals, '.', '*' and '+'."""

    def __init__(self, pattern: str):
        self.start_state = StartState()
        self.term_state = TerminationState()
        prev = self.start_state
        i = 0
        while i < len(pattern):
            c = pattern[i]
            if c == '.':
                state = DotState()
            else:
                state = AsciiState(c)
            if i+1 < len(pattern) and pattern[i+1] in ('*', '+'):
                quant = pattern[i+1]
                i += 2
                if quant == '*':
                    star = StarState()
                    prev.add_next(state)
                    state.add_next(star)
                    star.loop_state = state
                    prev.add_next(star)
                    prev = star
                else:
                    plus = PlusState()
                    prev.add_next(state)
                    state.add_next(plus)
                    plus.loop_state = state
                    prev = plus
            else:
                prev.add_next(state)
                prev = state
                i += 1
        prev.add_next(self.term_state)

    def check_string(self, s: str):
        """Return True if the entire string matches the pattern."""
        def closure(states):
            stack = list(states)
            result = set(states)
            while stack:
                st = stack.pop()
                if isinstance(st, (StartState, StarState, PlusState)):
                    for nxt in st.next_states:
                        if nxt not in result:
                            result.add(nxt)
                            stack.append(nxt)
            return result

        active = closure({self.start_state})
        if self.start_state in active:
            active.remove(self.start_state)

        for ch in s:
            next_active = set()
            for st in active:
                if st.check_self(ch):
                    for nxt in st.next_states:
                        next_active.add(nxt)
                if isinstance(st, StarState) and st.loop_state.check_self(ch):
                    next_active.add(st)
                if isinstance(st, PlusState) and st.loop_state.check_self(ch):
                    next_active.add(st)
            active = closure(next_active)

        active = closure(active)
        return self.term_state in active

if __name__ == "__main__":
    regex_compiled = RegexFSM("a*4.+hi")
    assert regex_compiled.check_string("aaaaaa4uhi") == True
    assert regex_compiled.check_string("4uhi") == True
    assert regex_compiled.check_string("meow") == False
    assert regex_compiled.check_string("a4/hi") == True
