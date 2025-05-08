# Custom Regular Expression Engine

This project implements a custom regular expression engine using a Finite State Machine (FSM) approach. I've rewritten the structure to make it more modular and maintainable.

## Overview

The implementation provides a lightweight regex engine that supports basic regular expression operations:

- Literal character matching
- Wildcard (`.`) for matching any single character
- Star (`*`) quantifier for matching zero or more occurrences
- Plus (`+`) quantifier for matching one or more occurrences

## How It Works

The implementation uses a Finite State Machine approach where:

1. **States**: Different types of states handle specific matching behaviors:
   - `StartState`: Marks the beginning of pattern matching
   - `TerminationState`: Indicates successful pattern completion
   - `AsciiState`: Matches a specific literal character
   - `DotState`: Matches any single character (`.`)
   - `StarState`: Implements the `*` quantifier logic
   - `PlusState`: Implements the `+` quantifier logic

2. **Pattern Compilation**: The `RegexFSM` class parses a regex pattern and constructs the corresponding state machine with appropriate transitions.

3. **Matching Algorithm**: The `check_string` method traverses the state machine using a set of active states, handling transitions and closures to determine if a string matches the pattern.

4. **ε-transitions**: The implementation handles epsilon transitions (transitions without consuming input) for operations like `*` and `+` through the closure method.

## How to Run

### Requirements
- Python 3.12

### Usage

1. Import the module in your Python code:
   ```python
   from regex import RegexFSM
   ```

2. Create a regex pattern:
   ```python
   pattern = RegexFSM("a*b.+c")
   ```

3. Check if strings match the pattern:
   ```python
   result = pattern.check_string("abbxc")  # Returns True or False
   ```

### Running the Example

The module includes a simple test case that you can run directly:

```bash
python regex.py
```

This will execute the test assertions at the bottom of the file:
```python
regex_compiled = RegexFSM("a*4.+hi")
assert regex_compiled.check_string("aaaaaa4uhi") == True
assert regex_compiled.check_string("4uhi") == True
assert regex_compiled.check_string("meow") == False
assert regex_compiled.check_string("a4/hi") == True
```

## Limitations

This implementation supports only a subset of regex features. It doesn't include:
- Character classes (`[abc]`)
- Escape sequences
- Capture groups
- Boundary assertions
- Alternation (`|`)

## License

This project is licensed under the Mozilla Public License Version 2.0 - see the LICENSE file for details.
