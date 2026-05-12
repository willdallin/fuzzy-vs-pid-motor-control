import numpy as np
import skfuzzy.control as ctrl

class FuzzyController:
    def __init__(self):
        self.error = ctrl.Antecedent(np.arange(-100, 101, 1), 'error')
        self.delta_error = ctrl.Antecedent(np.arange(-50, 51, 1), 'delta_error')

        self.voltage_change = ctrl.Consequent(np.arange(-0.5, 0.51, 0.01), 'voltage_change')

        self.error.automf(names=['NB', 'NS', 'ZE', 'PS', 'PB'])
        self.delta_error.automf(names=['NB', 'NS', 'ZE', 'PS', 'PB'])
        self.voltage_change.automf(names=['NB', 'NS', 'ZE', 'PS', 'PB'])

        self._build_rules()
        self.control_system = ctrl.ControlSystem(self.rules)
        self.simulator = ctrl.ControlSystemSimulation(self.control_system)
        self.current_voltage = 0.0

    def _build_rules(self):
        e = self.error
        de = self.delta_error
        vc = self.voltage_change

        self.rules = [
            ctrl.Rule(e['NB'] & de['NB'], vc['NB']),
            ctrl.Rule(e['NB'] & de['NS'], vc['NB']),
            ctrl.Rule(e['NB'] & de['ZE'], vc['NB']),
            ctrl.Rule(e['NB'] & de['PS'], vc['NS']),
            ctrl.Rule(e['NB'] & de['PB'], vc['ZE']),

            ctrl.Rule(e['NS'] & de['NB'], vc['NB']),
            ctrl.Rule(e['NS'] & de['NS'], vc['NS']),
            ctrl.Rule(e['NS'] & de['ZE'], vc['NS']),
            ctrl.Rule(e['NS'] & de['PS'], vc['ZE']),
            ctrl.Rule(e['NS'] & de['PB'], vc['PS']),

            ctrl.Rule(e['ZE'] & de['NB'], vc['NS']),
            ctrl.Rule(e['ZE'] & de['NS'], vc['NS']),
            ctrl.Rule(e['ZE'] & de['ZE'], vc['ZE']),
            ctrl.Rule(e['ZE'] & de['PS'], vc['PS']),
            ctrl.Rule(e['ZE'] & de['PB'], vc['PS']),

            ctrl.Rule(e['PS'] & de['NB'], vc['NS']),
            ctrl.Rule(e['PS'] & de['NS'], vc['ZE']),
            ctrl.Rule(e['PS'] & de['ZE'], vc['PS']),
            ctrl.Rule(e['PS'] & de['PS'], vc['PB']),
            ctrl.Rule(e['PS'] & de['PB'], vc['PB']),

            ctrl.Rule(e['PB'] & de['NB'], vc['ZE']),
            ctrl.Rule(e['PB'] & de['NS'], vc['PS']),
            ctrl.Rule(e['PB'] & de['ZE'], vc['PB']),
            ctrl.Rule(e['PB'] & de['PS'], vc['PB']),
            ctrl.Rule(e['PB'] & de['PB'], vc['PB'])
        ]

    def compute(self, error, delta_error):
        self.simulator.input['error'] = error
        self.simulator.input['delta_error'] = delta_error
        self.simulator.compute()
        
        delta_v = self.simulator.output['voltage_change']
        self.current_voltage = max(-24.0, min(24.0, self.current_voltage + delta_v))
        return self.current_voltage

    def reset(self):
        self.current_voltage = 0.0