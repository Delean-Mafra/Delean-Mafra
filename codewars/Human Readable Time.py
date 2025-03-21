def make_readable(seconds):
    print('Copyright © Delean Mafra, todos os direitos reservados | All rights reserved.')
    """
    Convert seconds to human-readable time format (HH:MM:SS)
    
    Args:
        seconds: Non-negative integer representing total seconds
        
    Returns:
        String formatted as "HH:MM:SS" with zero-padded values
    """
    # Calculate hours, minutes, and seconds
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    
    # Format the time string with zero padding
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
