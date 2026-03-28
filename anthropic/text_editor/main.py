def greeting():
    print("Hi there!")


def square_root(number):
    """
    Calculate the square root of a given number using Newton's method.
    
    Args:
        number: A non-negative number (int or float)
    
    Returns:
        The square root of the number
    
    Raises:
        ValueError: If the number is negative
        TypeError: If the input is not a number
    """
    # Input validation
    if not isinstance(number, (int, float)):
        raise TypeError("Input must be a number (int or float)")
    
    if number < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    
    # Handle special cases
    if number == 0:
        return 0
    if number == 1:
        return 1
    
    # Newton's method for square root calculation
    # Initial guess
    guess = number / 2.0
    epsilon = 1e-10  # Precision threshold
    
    while True:
        # Newton's formula: x_new = (x_old + number/x_old) / 2
        new_guess = (guess + number / guess) / 2
        
        # Check if we've reached desired precision
        if abs(new_guess - guess) < epsilon:
            return new_guess
        
        guess = new_guess