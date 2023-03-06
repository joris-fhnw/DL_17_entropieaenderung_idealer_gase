from CoolProp.CoolProp import PropsSI

# inputs in °C and bar
def h(t, p):
    p = p * 1e5
    T = t + 273.15
    return PropsSI("Hmass", "P", p, "T", T, "HEOS::Water") / 1e3


def u(t, p):
    p = p * 1e5
    T = t + 273.15
    return PropsSI("Umass", "P", p, "T", T, "HEOS::Water") / 1e3


def v(t, p):
    p = p * 1e5
    T = t + 273.15
    return 1 / PropsSI("D", "P", p, "T", T, "HEOS::Water")


def s(t, p):
    p = p * 1e5
    T = t + 273.15
    return PropsSI("Smass", "P", p, "T", T, "HEOS::Water") / 1e3

