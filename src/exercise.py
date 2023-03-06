from typing import List

from matplotlib.figure import Figure
from matplotlib.pyplot import Axes
from pytm import AbstractExercise
from pytm import Latex
from pytm import Option
from pytm import Output

from .helpers import *
from .steamCharts import *
from CoolProp.CoolProp import PropsSI
import CoolProp
HEOS = CoolProp.AbstractState('HEOS', 'Water')

class Exercise(AbstractExercise):
    def start(self,teilaufgabe: float = None, W12: str = None,Q12: str = None) -> Output:
        options: List[Option] = list(map(lambda opt: Option(opt[0], Latex(opt[0]), opt[0] == teilaufgabe ),
                                         self._get_option_map()))

        return self.output \
            .add_paragraph(Latex(r'''
            Eine Kolben-Zylinder-Anordnung enthält 1 kg Wasser, anfänglich bei T1 = 200 °C und einen Druck von 0.7 MPa
             (7 bar). Das Wasser im Zylinder durchläuft einen Prozess bei konstantem Druck bis am Ende 100% gesättigte 
             Flüssigkeit vorhanden ist. Vernachlässigen Sie die kinetischen und potenziellen Energiedifferenzen in der 
             Energiebilanz. \ 
             a.) Skizzieren Sie das p-v-Diagramm, welches die Zustände und den Prozess zeigt.\
             b.) Bestimmen Sie die Arbeit und die Wärmeübertragung für den Prozess, in kJ. Achten Sie auf die 
             Vorzeichen der beiden Energieübertragungen. \
            ''')) \
            .add_option_group(name='teilaufgabe',
                          label=Latex(r'Wählen Sie aus, von welcher Teilaufgabe sie die Lösung sehen wollen:'),
                          options=options,
                          inline=False) \
            .add_number_field(name='W12',
                              label=Latex(r'Tragen Sie die Lösung für v1 in [m3/kg] ein'),
                              value=W12) \
            .add_number_field(name='Q12',
                              label=Latex(r'Tragen Sie die Lösung für v1 in [m3/kg] ein'),
                              value=Q12) \
             .add_action('Calculate', self.calculate)

    # .add_number_field(name='temp',
    #                   label=Latex(r'Tragen Sie die Temperatur ein, in °C'),
    #                   value=temp,
    #                   min_value=-60,
    #                   max_value=2200,
    #                   step=0.01) \



    def calculate(self,teilaufgabe: str,W12: str, Q12: str) -> Output:
        teilaufgabe_test = list(filter(lambda config: config[0] == teilaufgabe, self._get_option_map()))[0]
        T_norm = 273.15
        m = 1 # [kg]
        T1 = 200  # [°C]
        p1 = 7  #  [bar]
        p2 = p1  #  [bar]
        T2 = PropsSI("T", "P", p2 * 1e5, "Q", 0, "HEOS::Water") - T_norm  # [°C]

        pt1 = steamCharts_ed8.SteamCharts(T1, p1)
        pt2 = steamCharts_ed8.SteamCharts(T2, p2)
        v2 = 1 / PropsSI('D', 'P', p2 * 1e5, 'Q', 0, 'Water')  # gesättigt
        u2 = PropsSI('Umass','P',7*1e5,'Q',0,'Water')*1e-3  # [kJ/kg]
        v1 = A3_stem.v(T1, p1)
        u1 = A3_stem.u(T1,p1)
        W12_ca = -m*p1*1e5*(v2-v1)*1e-3  # [kJ]
        dU = m*(u2-u1)  # [kJ]
        Q12_ca = dU-W12_ca  # [kJ]

        if teilaufgabe_test[0] == "a":

            figure = steamChartPlot.p_v_plot_2(pt1,pt2)
            return self.output \
                .add_paragraph(Latex(r'''
                Text 1
                ''')) \
                .add_paragraph(Latex(r'''
                Text 2
                ''')) \
                .add_figure(figure) \
                .add_action('Back to start', self.start, teilaufgabe=teilaufgabe, W12 = W12, Q12 = Q12)
        else:
            if abs(W12-W12_ca) <= 3:
                answ1 = "Die Arbeit wurde richtig berechnet!!\n"
                print(abs(W12-W12_ca))
                print("Die Arbeit wurde richtig berechnet!!\n")
            else:
                answ1 = f"die Arbeit wurde falsch berechnet, die richtige Lösung ist: {round(W12_ca)} kJ"
                print(abs(W12 - W12_ca))
                print("falsch...\n")

            if abs(Q12-Q12_ca) <= 3:
                answ2 = "Die Wärme wurde richtig berechnet!!\n"
                print(abs(Q12-Q12_ca))
                print("Die Wärme wurde richtig berechnet!!\n")
            else:
                answ2 = f"die Arbeit wurde falsch berechnet, die richtige Lösung ist: {round(Q12_ca)} kJ"
                print(abs(Q12 - Q12_ca))
                print("falsch...\n")
            # Um die Arbeit zu berechnen, wird v1 und v2 (in [m3/kg]) benötigt
            return self.output \
            .add_paragraph(Latex(answ1)) \
            .add_paragraph(Latex(answ2)) \
            .add_action('Back to start', self.start, teilaufgabe=teilaufgabe,W12 = W12, Q12 = Q12)


        # .add_action('Back to start', self.start, gas=gas, temp=temp)


    @staticmethod
    def _get_option_map() -> list:
        return [
            ["a"],
            ["b"],
        ]


    # @staticmethod
    # def _get_option_map() -> list:
    #     return [
    #         ['Air', r'Air', Cp_ave_Air, s_abs_Air],
    #         ['N2s', r'Luftstickstoff', Cp_ave_N2s, s_abs_N2s],
    #         ['N2', r'$\mathrm{N_{2}}$', Cp_ave_N2, s_abs_N2],
    #         ['O2', r'$\mathrm{O_{2}}$', Cp_ave_O2, s_abs_O2],
    #         ['CO2', r'$\mathrm{CO_{2}}$', Cp_ave_CO2, s_abs_CO2],
    #         ['H2O', r'$\mathrm{H_{2}O}$', Cp_ave_H2O, s_abs_H2O],
    #         ['SO2', r'$\mathrm{SO_{2}}$', Cp_ave_SO2, s_abs_SO2],
    #     ]