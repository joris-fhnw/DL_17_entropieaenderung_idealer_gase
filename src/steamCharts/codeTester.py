import steamChartPlot
import steamCharts_ed8
from CoolProp.CoolProp import PropsSI
import A3_stem
import CoolProp
from matplotlib.figure import Figure
from matplotlib.pyplot import Axes
import numpy as np

"Hier kann der code unabhängig vom LTI-Tool getestet werden"

HEOS = CoolProp.AbstractState('HEOS', 'Water')
Tc = PropsSI("Tcrit", "Water")
Pc = PropsSI("Pcrit", "Water")

T_norm = 273.15
T1 = 500
p1 = 100
p2 = p1
T2 = PropsSI("T", "P", p2*1e5, "Q", 0, "HEOS::Water")-T_norm

pt1 = steamCharts_ed8.SteamCharts(T1,p1)
pt2 = steamCharts_ed8.SteamCharts(T2,p2)

m=1
v2 = 1 / PropsSI('D', 'P', p2 * 1e5, 'Q', 0, 'Water')  # gesättigt
u2 = PropsSI('Umass', 'P', 7 * 1e5, 'Q', 0, 'Water') * 1e-3  # [kJ/kg]

v1 = A3_stem.v(T1, p1)
u1 = A3_stem.u(T1, p1)
W12_ca = -m * p1 * 1e5 * (v2 - v1) * 1e-3  # [kJ]
dU = m * (u2 - u1)  # [kJ]
Q12_ca = dU - W12_ca  # [kJ]

# steamChartPlot.p_v_plot(pt1,pt2)

# Press = np.linspace(pt1.p + pt1.p_under, pt1.p + pt1.p_over, 200)
#
# figure: Figure = Figure()
# plot1: Axes = figure.add_subplot(2, 1, 1)
# # plotting the isotherm in P_v diagram
# plot1.semilogx(1 / PropsSI("D", "P", Press, "T", pt1.T, "HEOS::Water"), Press / 1e5,
#                label='Temperature = ' + str(pt1.T) + ' K, ')
# if pt1.saturated == 'False':
#     plot1.semilogx(1 / PropsSI("D", "P", pt1.p, "T", pt1.T, "HEOS::Water"), pt1.p / 1e5, 'ro', \
#                    label='P = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(pt1.T) + ' K')
# else:
#     v = 1 / PropsSI('D', 'P', pt1.p, 'Q', 0,
#                     'Water')  # float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
#     plot1.semilogx(v, pt1.p / 1e5, 'ro',
#                    label='P = ' + str(pt1.p / 1e5) + ' bar, ' + 'T = ' + str(pt1.T) + ' K')
#
# Press2 = np.linspace(pt2.p + pt2.p_under, pt2.p + pt2.p_over, 200)
# # plotting the isotherm in P_v diagram
# plot1.semilogx(1 / PropsSI("D", "P", Press2, "T", pt2.T, "HEOS::Water"), Press2 / 1e5,
#                label='Temperature = ' + str(pt2.T) + ' K, ')
# if pt2.saturated == 'False':
#     plot1.semilogx(1 / PropsSI("D", "P", pt2.p, "T", pt2.T, "HEOS::Water"), pt2.p / 1e5, 'ro', \
#                    label='P = ' + str(pt2.p / 1e5) + ' bar, ' + 'T = ' + str(pt2.T) + ' K')
# else:
#     v = 1 / PropsSI('D', 'P', pt2.p, 'Q', 0,
#                     'Water')  # float(input('The state is saturated. Enter the speoific volume in m^3/kg '))
#     plot1.semilogx(v, pt2.p / 1e5, 'ro',
#                    label='P = ' + str(pt2.p / 1e5) + ' bar, ' + 'T = ' + str(pt2.T) + ' K')
#
# # plotting the saturation states
# P_range = np.logspace(np.log10(611), np.log10(Pc), 1000)  # 611 is just above the triple point pressure
# V_liquid = 1 / PropsSI("D", "P", P_range, "Q", 0, "HEOS::Water")
# V_vapor = 1 / PropsSI("D", "P", P_range, "Q", 1, "HEOS::Water")
# plot1.semilogx(V_liquid, P_range / 1e5)
# plot1.semilogx(V_vapor, P_range / 1e5)
# # plot1.gca().set_ylim(bottom=0)  # had problems with neg. pressures when above critical pt
#
# plot1.set_xlabel('specific Volume (v) in m^3/kg')
# plot1.set_ylabel('Pressure [bar]')
# plot1.legend(loc='best')

# # steamChartPlot.T_v_plot(pt1,pt2)