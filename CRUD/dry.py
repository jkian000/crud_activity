PI = 3.14159

def calculate_circle_area(radius):
    return PI * radius * radius

def calculate_circle_circumference(radius):
    return 2 * PI * radius

def print_circle_properties(radius):
    area = calculate_circle_area(radius)
    circumference = calculate_circle_circumference(radius)
    print(f"Circle with radius {radius} has area {area} and circumference {circumference}")