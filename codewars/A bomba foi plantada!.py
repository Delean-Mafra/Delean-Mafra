from collections import deque

def bfs(m, start, goal):
    rows, cols = len(m), len(m[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    queue = deque([(start[0], start[1], 0)])
    visited = set()
    visited.add(start)
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")

    
    while queue:
        x, y, dist = queue.popleft()
        
        if (x, y) == goal:
            return dist
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and m[nx][ny] != 'X':
                queue.append((nx, ny, dist + 1))
                visited.add((nx, ny))
    
    return float('inf')

def bomb_has_been_planted(m, time):
    ct_pos = bomb_pos = kit_pos = None
    
    # Locate the CT, bomb, and kit positions
    for r in range(len(m)):
        for c in range(len(m[0])):
            if m[r][c] == 'CT':
                ct_pos = (r, c)
            elif m[r][c] == 'B':
                bomb_pos = (r, c)
            elif m[r][c] == 'K':
                kit_pos = (r, c)
    
    if not ct_pos or not bomb_pos:
        return False
    
    # Calculate distance from CT to bomb
    dist_ct_to_bomb = bfs(m, ct_pos, bomb_pos)
    
    # If there's a kit, calculate distance to kit and then to bomb
    if kit_pos:
        dist_ct_to_kit = bfs(m, ct_pos, kit_pos)
        dist_kit_to_bomb = bfs(m, kit_pos, bomb_pos)
    else:
        dist_ct_to_kit = dist_kit_to_bomb = float('inf')
    
    # Scenario 1: Directly defuse the bomb without the kit
    time_needed_without_kit = dist_ct_to_bomb + 10
    
    # Scenario 2: Use the kit to defuse the bomb
    time_needed_with_kit = dist_ct_to_kit + dist_kit_to_bomb + 5
    
    # Check if either scenario is possible within the given time
    return time_needed_without_kit <= time or time_needed_with_kit <= time

# Test cases
print(bomb_has_been_planted(
    [
        ["0", "0", "0", "0", "B"],
        ["0", "0", "0", "0", "CT"],
        ["0", "0", "0", "0", "0"],
        ["0", "K", "0", "0", "0"],
    ],
    14
))  # Output: True

print(bomb_has_been_planted(
    [
        ["CT", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0", "0", "B"],
    ],
    10
))  # Output: False
