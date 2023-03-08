import matplotlib.pyplot as plt
import CoolProp
from CoolProp.CoolProp import PropsSI
import numpy as np
from matplotlib.figure import Figure
from matplotlib.pyplot import Axes


HEOS = CoolProp.AbstractState('HEOS', 'Water')
Tc = PropsSI("Tcrit", "Water")
Pc = PropsSI("Pcrit", "Water")


def p_v_plot_2(pt1,pt2):
    Press = np.linspace(pt1.p + pt1.p_under, pt1.p + pt1.p_over, 200)
    figure: Figure = Figure()
    plot1: Axes = figure.add_subplot(2, 1, 1)
    # plotting the isotherm in P_v diagram
    plot1.semilogx(1 / PropsSI("D", "P", Press, "T", pt1.T, "HEOS::Water"), Press / 1e5,
                   label='Temperature = '+str(round(pt1.T-273.15,2)) + '° C')
    if pt1.saturated == 'False':
        plot1.semilogx(1 / PropsSI("D", "P", pt1.p, "T", pt1.T, "HEOS::Water"), pt1.p / 1e5, 'ro', \
                       label='P1 = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(round(pt1.T-273.15,2)) + '° C')
    else:
        v = 1 / PropsSI('D', 'P', pt1.p, 'Q', 0,
                        'Water')  # float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
        plot1.semilogx(v, pt1.p / 1e5, "ro",
                       label='P1 = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(round(pt1.T-273.15,2)) + '° C')

    Press2 = np.linspace(pt2.p + pt2.p_under, pt2.p + pt2.p_over, 200)
    # plotting the isotherm in P_v diagram
    plot1.semilogx(1 / PropsSI("D", "P", Press2, "T", pt2.T, "HEOS::Water"), Press2 / 1e5,
                   label='Temperature = ' + str(round(pt2.T-273.15,2)) + ' °C, ')
    if pt2.saturated == 'False':
        plot1.semilogx(1 / PropsSI("D", "P", pt2.p, "T", pt2.T, "HEOS::Water"), pt2.p / 1e5, 'co',
                       label='P2 = ' + str(round(pt2.p / 1e5,2)) + ' bar, ' + 'T = ' + str(round(pt2.T-273.15,2)) + '° C')
    else:
        v = 1 / PropsSI('D', 'P', pt2.p, 'Q', 0,
                        'Water')  # float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
        plot1.semilogx(v, pt2.p / 1e5, "co",
                       label='P2 = ' + str(round(pt2.p / 1e5,2)) + ' bar, ' + 'T = ' + str(round(pt2.T-273.15,2)) + '° C')

    # plotting the saturation states
    P_range = np.logspace(np.log10(611), np.log10(Pc), 1000)  # 611 is just above the triple point pressure
    V_liquid = 1 / PropsSI("D", "P", P_range, "Q", 0, "HEOS::Water")
    V_vapor = 1 / PropsSI("D", "P", P_range, "Q", 1, "HEOS::Water")
    plot1.semilogx(V_liquid, P_range / 1e5, color = "black")
    plot1.semilogx(V_vapor, P_range / 1e5,color = "black")
    plot1.set_ylim(bottom=0)  # had problems with neg. pressures when above critical pt

    plot1.set_xlabel('specific Volume (v) in m^3/kg')
    plot1.set_ylabel('Pressure [bar]')
    plot1.legend(loc='best')

    return figure


def T_v_plot(pt1,pt2):

    Temps = np.linspace(pt1.T1_sat + pt1.T_under, pt1.T + pt1.T_over, 200)
    fig = plt.figure()
    # plotting the isobar in T_v diagram
    plt.semilogx(1 / PropsSI("D", "P", pt1.p, "T", Temps, "HEOS::Water"), Temps,
                 label='Pressure = ' + str(pt1.p / 1e5) + ' bar, ')
    if pt1.saturated == 'False':
        plt.semilogx(1 / PropsSI("D", "P", pt1.p, "T", pt1.T, "HEOS::Water"), pt1.T, 'ro', \
                     label='P = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(pt1.T) + ' K')
    else:
        v = 1/PropsSI('D','P',pt1.p,'Q',0,'Water')#float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
        plt.semilogx(v, pt1.T, 'ro', label='P = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(pt1.T) + ' K')

    Temps2 = np.linspace(pt2.T1_sat + pt2.T_under, pt2.T + pt2.T_over, 200)
    # plotting the isobar in T_v diagram
    plt.semilogx(1 / PropsSI("D", "P", pt2.p, "T", Temps2, "HEOS::Water"), Temps,
                 label='Pressure = ' + str(pt2.p / 1e5) + ' bar, ')
    if pt2.saturated == 'False':
        plt.semilogx(1 / PropsSI("D", "P", pt2.p, "T", pt2.T, "HEOS::Water"), pt2.T, 'ro', \
                     label='P = ' + str(pt2.p / 1e5) + ' bar, ' + 'T = ' + str(pt2.T) + ' K')
    else:
        v = 1/PropsSI('D','P',pt2.p,'Q',0,'Water') #float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
        plt.semilogx(v, pt2.T, 'ro', label='P = ' + str(pt2.p / 1e5) + ' bar, ' + 'T = ' + str(pt2.T) + ' K')

    # plotting the saturation states // 2-Phasen Diagramm
    Tc = PropsSI("Tcrit", "Water")
    T_range = np.linspace(273.16, Tc, 200)
    V_liquid = 1 / PropsSI("D", "T", T_range, "Q", 0, "HEOS::Water")
    V_vapor = 1 / PropsSI("D", "T", T_range, "Q", 1, "HEOS::Water")
    plt.semilogx(V_liquid, T_range)
    plt.semilogx(V_vapor, T_range)

    plt.xlabel('specific Volume (v) in m^3/kg')
    plt.ylabel('Temperature [deg K]')
    plt.legend(loc='best')
    plt.show(block=False)
    
    
def p_v_plot(pt1,pt2):
    Press = np.linspace(pt1.p + pt1.p_under, pt1.p + pt1.p_over, 200)
    fig = plt.figure()
    # plotting the isotherm in P_v diagram
    plt.semilogx(1 / PropsSI("D", "P", Press, "T", pt1.T, "HEOS::Water"), Press / 1e5,
                 label='Temperature = ' + str(pt1.T) + ' K, ')
    if pt1.saturated == 'False':
        plt.semilogx(1 / PropsSI("D", "P", pt1.p, "T", pt1.T, "HEOS::Water"), pt1.p / 1e5, 'ro', \
                     label='P = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(pt1.T) + ' K')
    else:
        v = 1/PropsSI('D','P',pt1.p,'Q',0,'Water')#float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
        plt.semilogx(v, pt1.p / 1e5, 'ro',
                     label='P = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(pt1.T) + ' K')

    Press2 = np.linspace(pt2.p + pt2.p_under, pt2.p + pt2.p_over, 200)
    # plotting the isotherm in P_v diagram
    plt.semilogx(1 / PropsSI("D", "P", Press2, "T", pt2.T, "HEOS::Water"), Press2 / 1e5,
                 label='Temperature = ' + str(pt2.T) + ' K, ')
    if pt2.saturated == 'False':
        plt.semilogx(1 / PropsSI("D", "P", pt2.p, "T", pt2.T, "HEOS::Water"), pt2.p / 1e5, 'ro', \
                     label='P = ' + str(pt2.p / 1e5) + ' bar, ' + 'T = ' + str(pt2.T) + ' K')
    else:
        v = 1/PropsSI('D','P',pt2.p,'Q',0,'Water')#float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
        plt.semilogx(v, pt2.p / 1e5, 'ro',
                     label='P = ' + str(pt2.p / 1e5) + ' bar, ' + 'T = ' + str(pt2.T) + ' K')

    # plotting the saturation states
    P_range = np.logspace(np.log10(611), np.log10(Pc), 1000)  # 611 is just above the triple point pressure
    V_liquid = 1 / PropsSI("D", "P", P_range, "Q", 0, "HEOS::Water")
    V_vapor = 1 / PropsSI("D", "P", P_range, "Q", 1, "HEOS::Water")
    plt.semilogx(V_liquid, P_range / 1e5)
    plt.semilogx(V_vapor, P_range / 1e5)
    plt.gca().set_ylim(bottom=0)  # had problems with neg. pressures when above critical pt

    plt.xlabel('specific Volume (v) in m^3/kg')
    plt.ylabel('Pressure [bar]')
    plt.legend(loc='best')
    plt.show(block=False)