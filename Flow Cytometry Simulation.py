import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import gaussian_kde

class FlowCytometrySimulator:
    def __init__(self):
        # Initialize with multiple cell populations
        self.populations = {
            'lymphocytes': {
                'size': (8, 1.5),
                'complexity': (15, 2),
                'fl1': (30, 5),
                'fl2': (10, 2),
                'proportion': 0.6
            },
            'monocytes': {
                'size': (15, 3),
                'complexity': (25, 3),
                'fl1': (60, 8),
                'fl2': (30, 5),
                'proportion': 0.3
            },
            'granulocytes': {
                'size': (20, 4),
                'complexity': (35, 4),
                'fl1': (40, 6),
                'fl2': (50, 7),
                'proportion': 0.1
            }
        }
        self.total_cells = 10000
        self._validate_population_proportions()
        
    def _validate_population_proportions(self):
        total = sum(p['proportion'] for p in self.populations.values())
        if not np.isclose(total, 1.0):
            raise ValueError("Population proportions must sum to 1")

    def simulate(self):
        data = []
        for pop_name, params in self.populations.items():
            n = int(self.total_cells * params['proportion'])
            
            pop_data = {
                'FSC': np.random.normal(*params['size'], n),
                'SSC': np.random.normal(*params['complexity'], n),
                'FL1': np.random.normal(*params['fl1'], n),
                'FL2': np.random.normal(*params['fl2'], n),
                'Population': pop_name
            }
            
            # Add 10% double positive cells
            mask = np.random.rand(n) < 0.1
            pop_data['FL1'][mask] += np.random.normal(20, 5, mask.sum())
            pop_data['FL2'][mask] += np.random.normal(20, 5, mask.sum())
            
            data.append(pd.DataFrame(pop_data))
        
        self.data = pd.concat(data, ignore_index=True)
        self._add_compensation()
        return self.data
    
    def _add_compensation(self):
        # Simulate spectral overlap between channels
        self.data['FL1'] += 0.1 * self.data['FL2']
        self.data['FL2'] += 0.05 * self.data['FL1']

    def visualize(self, log_scale=True):
        if not hasattr(self, 'data'):
            raise ValueError("Simulate data first using .simulate()")
            
        fig, ax = plt.subplots(2, 2, figsize=(12, 10))
        
        # FSC vs SSC
        self._plot_density(ax[0,0], 'FSC', 'SSC', log_scale)
        # FL1 vs FL2
        self._plot_density(ax[0,1], 'FL1', 'FL2', log_scale)
        # FSC histogram
        self._plot_histogram(ax[1,0], 'FSC')
        # FL1 histogram
        self._plot_histogram(ax[1,1], 'FL1')
        
        plt.tight_layout()
        plt.show()

    def _plot_density(self, ax, x_channel, y_channel, log_scale):
        for pop_name, group in self.data.groupby('Population'):
            x = group[x_channel]
            y = group[y_channel]
            
            if log_scale:
                x = np.log10(x.clip(1))
                y = np.log10(y.clip(1))
            
            # Calculate density
            xy = np.vstack([x, y])
            z = gaussian_kde(xy)(xy)
            
            ax.scatter(x, y, c=z, s=1, label=pop_name, alpha=0.5)
        
        ax.set_xlabel(x_channel + (' (log)' if log_scale else ''))
        ax.set_ylabel(y_channel + (' (log)' if log_scale else ''))
        ax.legend()
        ax.grid(True)

    def _plot_histogram(self, ax, channel):
        bins = np.linspace(self.data[channel].min(), self.data[channel].max(), 100)
        for pop_name, group in self.data.groupby('Population'):
            ax.hist(group[channel], bins=bins, alpha=0.5, label=pop_name)
        ax.set_xlabel(channel)
        ax.set_ylabel('Count')
        ax.legend()

    def set_parameters(self):
        print("Available populations:", list(self.populations.keys()))
        pop = input("Select population to modify: ")
        if pop not in self.populations:
            print("Invalid population!")
            return
            
        params = self.populations[pop]
        print(f"Current parameters for {pop}:")
        for param, value in params.items():
            if param != 'proportion':
                print(f"  {param}: mean={value[0]}, sd={value[1]}")
            else:
                print(f"  proportion: {value}")
        
        print("\nEnter new values (leave blank to keep current):")
        params['size'] = (
            float(input(f"New size mean ({params['size'][0]}): ") or params['size'][0]),
            float(input(f"New size sd ({params['size'][1]}): ") or params['size'][1])
        )
        params['complexity'] = (
            float(input(f"New complexity mean ({params['complexity'][0]}): ") or params['complexity'][0]),
            float(input(f"New complexity sd ({params['complexity'][1]}): ") or params['complexity'][1])
        )
        new_prop = float(input(f"New proportion ({params['proportion']}): ") or params['proportion'])
        
        # Update proportions
        old_prop = params['proportion']
        params['proportion'] = new_prop
        remaining = 1 - new_prop
        other_pops = [p for p in self.populations.values() if p != params]
        total_other = sum(p['proportion'] for p in other_pops)
        for p in other_pops:
            p['proportion'] = p['proportion'] / total_other * remaining
        
        self._validate_population_proportions()
        print("Parameters updated!")

# Main interaction loop
if __name__ == "__main__":
    simulator = FlowCytometrySimulator()
    
    while True:
        action = input("\nChoose action: [simulate/visualize/parameters/quit] ").lower()
        
        if action == 'simulate':
            data = simulator.simulate()
            print(f"Generated {len(data)} cells with distribution:")
            print(data['Population'].value_counts(normalize=True))
            
        elif action == 'visualize':
            log_choice = input("Use logarithmic scale? [y/n] ").lower()
            simulator.visualize(log_scale=(log_choice == 'y'))
            
        elif action == 'parameters':
            simulator.set_parameters()
            
        elif action == 'quit':
            break
            
        else:
            print("Invalid option. Please choose simulate/visualize/parameters/quit")