FlowCytometrySimulator

FlowCytometrySimulator is a Python program for simulating and visualizing synthetic flow cytometry data. It allows users to model multiple cell populations, generate realistic data distributions, and visualize flow cytometry plots.

Requirements
Python 3 with the following packages installed:

numpy
pandas
matplotlib
scipy

To install dependencies:
pip install numpy pandas matplotlib scipy

How to Run
Save the code in a notepad application to a Python file, for example flow_cytometry_simulator.py, and run it from the command prompt.

Features
Simulates flow cytometry data for three cell populations:
lymphocytes
monocytes
granulocytes

Produces forward scatter (FSC), side scatter (SSC), and two fluorescence channels (FL1 and FL2)
Models spectral overlap (spillover) between FL1 and FL2 channels

Provides interactive visualization:
FSC vs SSC density plot
FL1 vs FL2 density plot
Histograms for any channel

Allows modification of population parameters using a command-line interface.

Modes
simulate: Generates flow cytometry data with the current population settings.
visualize: Displays the generated data using scatter plots and histograms.
parameters: Allows you to interactively update cell population parameters such as size, complexity, fluorescence intensity, and proportions.

How It Works
Each population is defined by normal distributions for FSC, SSC, FL1, and FL2.
10% of each population is adjusted to simulate double-positive fluorescence signals.
Spectral overlap is applied by adding a portion of FL2 to FL1 and vice versa.
All generated data is stored in a Pandas DataFrame.

Customization
The set_parameters option allows users to:
Change the mean and standard deviation for: cell size (FSC), cell complexity (SSC), fluorescence channels (FL1, FL2).


Notes
This simulator can be used for:
Practicing data analysis for flow cytometry
Teaching and training on cytometry gating and visualization
Generating test datasets for software development
