from pytm import AbstractExercise
from pytm import Latex
from pytm import Output
import random
from .steamCharts import *
from CoolProp.CoolProp import PropsSI
import CoolProp
HEOS = CoolProp.AbstractState('HEOS', 'Water')



class Exercise(AbstractExercise):

    zahlen = [[200,7],[400,10],[800,30],[900,50],[500,100]]
    counter = 0
    def start(self, W12: str = None,Q12: str = None) -> Output:

        if Exercise.counter == 0:
            self.T,self.p = random.choice(Exercise.zahlen)
            Exercise.counter += 1


        return self.output \
            .add_paragraph(Latex(f'''
            Eine Kolben-Zylinder-Anordnung enthält 1 kg Wasser, anfänglich bei T1 = {self.T} °C und einen Druck von 
            {self.p/10} MPa ({self.p} bar). Das Wasser im Zylinder durchläuft einen Prozess bei konstantem Druck bis
             am Ende 100 Prozent gesättigte Flüssigkeit vorhanden ist. Vernachlässigen Sie die kinetischen und 
             potenziellen Energiedifferenzen in der Energiebilanz. \n
             a.) Skizzieren Sie das p-v-Diagramm, welches die Zustände und den Prozess zeigt.\n
             b.) Bestimmen Sie die Arbeit und die Wärmeübertragung für den Prozess, in kJ. Achten Sie auf die 
             Vorzeichen der beiden Energieübertragungen. \n
             \n
            ''')) \
            .add_number_field(name='W12',
                              label=Latex(r'Tragen Sie die Lösung für W12 in kJ ein'),
                              value=W12) \
            .add_number_field(name='Q12',
                              label=Latex(r'Tragen Sie die Lösung für Q12 in kJ ein'),
                              value=Q12) \
             .add_action('Loesung', self.loesung)\
             .add_paragraph("Um den Hinweis zu sehen, müssen Sie erst einen Zahlenwert (keine Buchstaben etc.,"
                            " in die beiden Antwortfelder eintragen)")\
             .add_action("Hinweis",self.hint)


    def hint(self,W12: str, Q12: str):
        hint1 = "-Die Arbeit ist hier Volumenänderungsarbeit, dazu benötigen Sie den konstanten Druck und die " \
                "spezifischen Volumen v1 und v2" \
                ""
        hint2 = "-Für die Wärmemenge verwenden Sie die Energiebilanz, die gerade berechnete Arbeit und die spezifischen"\
                " inneren Energien u1 und u2" \


        return self.output \
        .add_paragraph(Latex(hint1)) \
        .add_paragraph(Latex(hint2)) \
        .add_action('Zurück zur Aufgabenstellung', self.start,W12 = W12, Q12 = Q12)

    def loesung(self,W12: str, Q12: str) -> Output:
        T_norm = 273.15
        m = 1 # [kg]
        T1 = self.T
        p1 = self.p
        p2 = p1  #  [bar]
        score = 0  # Anzahl Punkte, welche der Student erhält

        T2 = PropsSI("T", "P", p2 * 1e5, "Q", 0, "HEOS::Water") - T_norm  # [°C]

        pt1 = steamCharts_ed8.SteamCharts(T1, p1)
        pt2 = steamCharts_ed8.SteamCharts(T2, p2)
        v2 = 1 / PropsSI('D', 'P', p2 * 1e5, 'Q', 0, 'Water')  # gesättigt
        u2 = PropsSI('Umass','P',p2*1e5,'Q',0,'Water')*1e-3  # [kJ/kg]
        v1 = A3_stem.v(T1, p1)
        u1 = A3_stem.u(T1,p1)
        W12_ca = -m*p1*1e5*(v2-v1)*1e-3  # [kJ]
        dU = m*(u2-u1)  # [kJ]
        Q12_ca = dU-W12_ca  # [kJ]

        figure = steamChartPlot.p_v_plot_2(pt1,pt2)# Erzeugen des log(p)-h-Diagramms

        if abs(W12-W12_ca) <= 3:
            answ1 = "Die Arbeit wurde richtig berechnet!!\n"
            print(abs(W12-W12_ca))
            score += 1
        else:
            answ1 = f"Die Arbeit wurde falsch berechnet, die richtige Lösung ist: {round(W12_ca)} kJ"
            print(abs(W12 - W12_ca))

        if abs(Q12-Q12_ca) <= 3:
            answ2 = "Die Wärme wurde richtig berechnet!!\n"
            score += 2
        else:
            answ2 = f"Die Wärme wurde falsch berechnet, die richtige Lösung ist: {round(Q12_ca)} kJ"
            print(abs(Q12 - Q12_ca))

        # Um die Arbeit zu berechnen, wird v1 und v2 (in [m3/kg]) benötigt
        return self.output \
        .add_paragraph(Latex("Da p1 = p2 ist, verschiebt sich der  Punkt horizontal zur x-Achse, bis zur Siedelinie")) \
        .add_figure(figure) \
        .add_paragraph(Latex(answ1)) \
        .add_paragraph(Latex(answ2)) \
        .add_action('Zurück zur Aufgabenstellung', self.start,W12 = W12, Q12 = Q12)

