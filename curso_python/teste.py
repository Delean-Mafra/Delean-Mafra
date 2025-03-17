import pyautogui
import pyperclip

# Get the mouse position
coordinates = pyautogui.position()
print("Copyright ©2025 | Delean Mafra, todos os direitos reservados.")


# Extract X and Y coordinates as strings
x_str = str(coordinates.x)
y_str = str(coordinates.y)

# Combine them into a single string (optional)
combined_string = f"X= {x_str}, Y= {y_str}"

# Copy the string(s) to the clipboard
pyperclip.copy(combined_string)  # Or copy x_str and y_str separately
