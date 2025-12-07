"""Luminance calculation utilities for colorblind test image generation."""


def srgb_to_linear(s: float) -> float:
    """Convert sRGB value (0-1) to linear RGB."""
    if s <= 0.04045:
        return s / 12.92
    else:
        return ((s + 0.055) / 1.055) ** 2.4


def linear_to_srgb(lin: float) -> float:
    """Convert linear RGB to sRGB value (0-1)."""
    if lin <= 0.0031308:
        return lin * 12.92
    else:
        return 1.055 * (lin ** (1/2.4)) - 0.055


def calculate_luminance(r: int, g: int, b: int) -> float:
    """Calculate luminance (Y) from sRGB values (0-255)."""
    r_lin = srgb_to_linear(r / 255.0)
    g_lin = srgb_to_linear(g / 255.0)
    b_lin = srgb_to_linear(b / 255.0)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def solve_g_for_luminance(r: int, b: int, y_target: float) -> int:
    """Solve for G value that achieves target luminance, given R and B."""
    r_lin = srgb_to_linear(r / 255.0)
    b_lin = srgb_to_linear(b / 255.0)
    
    g_lin = (y_target - 0.2126 * r_lin - 0.0722 * b_lin) / 0.7152
    g_lin = max(0.0, min(1.0, g_lin))
    g_srgb = linear_to_srgb(g_lin)
    
    return int(round(g_srgb * 255))


def match_luminance(fg_rgb: tuple, bg_rgb: tuple) -> tuple:
    """Adjust foreground G to match background luminance."""
    bg_luminance = calculate_luminance(*bg_rgb)
    new_g = solve_g_for_luminance(fg_rgb[0], fg_rgb[2], bg_luminance)
    return (fg_rgb[0], new_g, fg_rgb[2])
