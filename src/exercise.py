import numpy as np
from pytm import AbstractExercise
from pytm import Latex
from pytm import Output
import random
from .steamCharts import *
from CoolProp.CoolProp import PropsSI
import CoolProp
# import os
HEOS = CoolProp.AbstractState('HEOS', 'Water')



class Exercise(AbstractExercise):

    zahlen_1 = [[200,1],[400,2],[800,3],[900,4],[500,5]]
    zahlen_2 = [[850,7],[750,10],[650,30],[950,50],[550,50]]
    gase = ["CO2","N2","O2"]
    counter = 0
    def start(self, ds: str = None) -> Output:

        if Exercise.counter == 0:
            self.T1,self.p1 = random.choice(Exercise.zahlen_1)
            self.T2, self.p2 = random.choice(Exercise.zahlen_2)
            self.gas_string = random.choice(Exercise.gase)
            Exercise.counter += 1
            # path = os.getcwd()
            # path_parent = os.path.dirname(os.getcwd())
            # print(path)


        return self.output \
            .add_paragraph(Latex(f'''
            {self.gas_string} ändert die Temperatur von \(T_1\) =  {self.T1} °C und den Druck von \(p_1\) =  
            {self.p1} bar auf eine Temperatur von \(T_2\)=  {self.T2} °C  und den Druck von \(p_2\) = {self.p2} bar. \n
             Berechnen Sie die spezifische Entropieänderung des Gases, benutzen Sie dazu die gemittelten Cps 
             aus der Tabelle A-7-3\n
              \n
             \n
            ''')) \
            .add_number_field(name='ds',
                              label=Latex(r'Tragen Sie die Lösung für die spezifische Entropie in kJ/(kg*K) ein'),
                              value=ds) \
             .add_action('Lösung', self.loesung)\
             .add_paragraph("Um den Hinweis zu sehen, müssen Sie erst einen Zahlenwert (keine Buchstaben etc.,"
                            " in die das Antwortfeld eintragen)")\
             .add_action("Hinweis",self.hint)


    def hint(self,ds: str):
        hint1 = f"{self.gas_string} ist ein ideales Gas" \
                ""
        hint2 = f"Die Gaskonstante von {self.gas_string} lässt sich mit R/M berechnen. " \
                f"Achten Sie dabei auf die Einheiten! " \


        return self.output \
        .add_paragraph(Latex(hint1)) \
        .add_paragraph(Latex(hint2)) \
        .add_action('Zurück zur Aufgabenstellung', self.start,ds = ds)

    def loesung(self,ds: str) -> Output:
        T_norm = 273.15
        R = 8.314 # [J/(mol*K)]
        M = PropsSI("M", self.gas_string)  # [kg/mol]
        T1 = self.T1+ T_norm # [K]
        T2 = self.T2+T_norm # [K]
        T_mean = (T1+T2)/2 # [K]
        p1 = self.p1*1e5  # [Pa]
        p2 = self.p2*1e5  # [Pa]
        p_mean = (p1 + p2) / 2  # [Pa]
        score = 0  # Anzahl Punkte, welche die Studenten erhalten
        cp = PropsSI("C", "P", p_mean, "T", T_mean, self.gas_string)*1e-3  # [kJ/(kg*K)]
        R_gas = R/M # [J/(kg*K)]
        ds_ca = cp*np.log(T2/T1) - R_gas*1e-3*np.log(p2/p1) # [kJ/(kg*K)]

        pt1 = steamCharts_ed8.SteamCharts(self.T1, self.p1)
        pt2 = steamCharts_ed8.SteamCharts(self.T2, self.p2)

        figure = steamChartPlot.p_v_plot_2(pt1,pt2)# Erzeugen des log(p)-h-Diagramms

        if abs((ds-ds_ca)/ds_ca) <= 0.1:
            answ1 = "Die spezifische Entropie wurde richtig berechnet!!\n"
            answ2 = ""
            answ3 = ""
            answ4 = ""
            # print(abs(ds-ds_ca))
            # score += 1/3
        else:
            answ1 = f"Die spezifische Entropie wurde falsch berechnet"
            answ2 = f"die richtige Lösung ist: {round(ds_ca,2)} kJ/(kg*K)\n"
            answ3 = f"Die Gaskonstante von {self.gas_string} ist {round(R_gas,2)} J/(kg*K)\n"
            answ4 = f"Die mittlere spezifische Wärmekapazität ist {round(cp,2)} kJ/(kg*K)\n"

                    # f"Die mittlere Temperatur ist {round(T_mean)} K\n"\
                    # f"Der mittlere Druck ist {round(p_mean)} Pa\n"\
                    # f"Die mittlere spezifische Wärmekapazität ist {round(cp)} kJ/(kg*K)\n"

            # print(abs(ds-ds_ca))
        # C:\\Users\\joris.strassburg\PycharmProjects\\DL_17_entropieaenderung_idealer_gase\\static\\Herleitung.PNG
        #     path_parent = os.path.dirname(os.getcwd())
        #     print(path_parent)
        # .add_figure(figure) \

        return self.output \
        .add_paragraph(Latex(answ1)) \
        .add_image("static\\Herleitung.PNG")\
        .add_paragraph(answ2) \
        .add_paragraph(answ3)            \
        .add_paragraph(answ4) \
        .add_action('Zurück zur Aufgabenstellung', self.start,ds = ds)

