# coding: utf-8


class Printer:
    def __init__(self, ils):
        self.ils = ils

        print("Printer created.")

    def info(self):
        if not self.ils.algorithm:
            step = 0
        else:
            step = self.ils.algorithm.step
        print("========================================================================")
        if not self.ils.algorithm:
            print("Step : " + str(step) + "  (ALG Step : " + "INIT" + ")")
        else:
            print("Step : " + str(step) + "  (ALG Step : " + str(step / 2) + ")")
        print("----- Light ------------------------------------------------------------")
        print("│ ID │ Lum. │ Sig │ Neighbor │ Objective │ Penalty   │ ")
        for l in self.ils.lights:
            if step % 2 != 0:
                print("│ " + '{0:2d}'.format(l.id) + " │ " + '{0:4.0f}'.format(l.luminosity) + " │ "
                      + '{0:3d}'.format(l.signals[0]) + " │ " + '{:<8}'.format(l.neighbor) + " │ "
                      + '{0:9.0f}'.format(l.objective_function) + " │ "
                      + '{0:9.0f}'.format(l.objective_penalty) + " │ ")
            else:
                print("│ " + '{0:2d}'.format(l.id) + " │ " + '{0:4.0f}'.format(l.luminosity) + " │ "
                      + '{0:3d}'.format(l.signals[0]) + " │ " + '{:<8}'.format(l.neighbor) + " │ "
                      + '{0:9.0f}'.format(l.next_objective_function) + " │ "
                      + '{0:9.0f}'.format(l.next_objective_penalty) + " │ ")

        print("----- Sensor -----------------------------------------------------------")
        print("│ ID │ Ill. │ Tar. │ Att.   │ Conv.     │")
        for s in self.ils.sensors:
            print("│ " + '{0:2d}'.format(s.id) + " │ " + '{0:4.0f}'.format(s.illuminance) + " │ "
                  + '{0:4.0f}'.format(s.target) + " │ "
                  + '{:<6}'.format("Attend" if s.attendance else "-") + " │ "
                  + '{:<9}'.format("Converged" if s.convergence else "-") + " │ ")