import re
from collections import defaultdict, deque

def regex_divisible_by(n):
    if n == 1:
        return r'^[01]+$'
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


    # Create the states for the DFA
    states = {i: {} for i in range(n)}

    for state in range(n):
        for bit in '01':
            new_state = (state * 2 + int(bit)) % n
            states[state][bit] = new_state

    # Generate the regex for the DFA
    # The regex should start from any state and end in state 0

    def build_regex():
        if n == 2:
            return r'^(?:(0*0)|(0*10))+$'

        transitions = defaultdict(list)
        for state in states:
            for bit, next_state in states[state].items():
                transitions[next_state].append((bit, state))

        final_state = 0
        visited = set()
        queue = deque([(final_state, '')])
        patterns = []

        while queue:
            state, path = queue.popleft()
            if state == 0 and path:
                patterns.append(path)
            if state in visited:
                continue
            visited.add(state)
            for bit, prev_state in transitions[state]:
                queue.append((prev_state, bit + path))

        return '|'.join(f'(0*{pattern})' for pattern in patterns)

    regex = f'^(?:{build_regex()})+$'
    return regex

# Test the function
n = 2
regex = regex_divisible_by(n)
print(f"Regex for n = {n}: {regex}")
test_cases = ["6","8", "12", "11"]
for case in test_cases:
    print(f"{case}: {True if re.fullmatch(regex, case) else False}")

n = 3
regex = regex_divisible_by(n)
print(f"Regex for n = {n}: {regex}")
test_cases = ["0", "1", "6", "7", "9", "10", "11", "12", "100", "110", "111", "1000"]
for case in test_cases:
    print(f"{case}: {True if re.fullmatch(regex, case) else False}")

n = 4
regex = regex_divisible_by(n)
print(f"Regex for n = {n}: {regex}")
test_cases = ["8", "11","12"]
for case in test_cases:
    print(f"{case}: {True if re.fullmatch(regex, case) else False}")

n = 5
regex = regex_divisible_by(n)
print(f"Regex for n = {n}: {regex}")
test_cases = ["10", "11"]
for case in test_cases:
    print(f"{case}: {True if re.fullmatch(regex, case) else False}")

n = 6
regex = regex_divisible_by(n)
print(f"Regex for n = {n}: {regex}")
test_cases = ["12", "11"]
for case in test_cases:
    print(f"{case}: {True if re.fullmatch(regex, case) else False}")
