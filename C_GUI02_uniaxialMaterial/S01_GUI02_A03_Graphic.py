# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-06-04
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI02_A03_Graphic.py
COMENTARIOS:    Grafica plots.
"""
# %% [00] INTRODUCTION
# GUI en Jupyter Notebook ejecuta esta funcion para añadir curvas a graficas.


# %% [01] LIBRARIES
import numpy as np
import matplotlib.pyplot as plt


# %% [02] FUNCTIONS

# %%% [02-00] PLOT STRAIN VS STRESS MONOTONIC
def plot_strain_stress(data_array_x, color_x, label_x, xlabel_x, ylabel_x, grid_x, ax_x=None):
    # If no axes object is provided, create a new figure with the specified size and resolution
    if ax_x is None:
        fig_x = plt.figure(figsize=(5.5, 3.2), dpi=100)
        ax_x = fig_x.add_axes([0.145, 0.133, 0.805, 0.827])

    # Determine the number of plots based on the number of columns
    num_columns_x = data_array_x.shape[1]
    num_plots_x = num_columns_x // 2

    # Plot each pair of columns
    for i in range(num_plots_x):
        x_data_x = data_array_x[:, 2 * i]
        y_data_x = data_array_x[:, 2 * i + 1]
        if i == 0:
            ax_x.plot(x_data_x, y_data_x, color=color_x, label=label_x)
        else:
            ax_x.plot(x_data_x, y_data_x, color=color_x)

    # Add labels and grid
    ax_x.set_xlabel(xlabel_x)
    ax_x.set_ylabel(ylabel_x)
    if grid_x:
        ax_x.grid(True)

    # Automatically scale the axes limits based on the data
    ax_x.relim()
    ax_x.autoscale()

    # Show legend
    ax_x.legend()


# %%% TODO [02-01] PLOT INDEX VS STRAIN
def plot_index_strain(data_array_x, color_x, label_x, xlabel_x, ylabel_x, grid_x, load_type_x, ax_x=None):
    # If no axes object is provided, create a new figure with the specified size and resolution
    if ax_x is None:
        fig_x = plt.figure(figsize=(11, 3.2), dpi=100)

        cx_1 = 0.0725
        wx_1 = 0.4025
        cx_2 = 0.5765
        wx_2 = 0.4025
        ax1_x = fig_x.add_axes([cx_1, 0.133, wx_1, 0.827])
        ax2_x = fig_x.add_axes([cx_2, 0.133, wx_2, 0.827])

    else:
        ax1_x, ax2_x = ax_x

    # PLOT AX1 ################################################################
    # Determine the number of plots based on the number of columns
    num_columns_x = data_array_x.shape[1]
    num_plots_x = num_columns_x // 2

    # Plot each pair of columns
    for i in range(num_plots_x):
        x_data_x = data_array_x[:, 2 * i]
        indices = np.arange(x_data_x.size)
        y_data_x = data_array_x[:, 2 * i + 1]
        if i == 0:
            ax1_x.plot(x_data_x, y_data_x, color=color_x, label=label_x)
            if load_type_x == 'cyclic':
                ax2_x.plot(indices, x_data_x, color=color_x, label=label_x)
        else:
            ax1_x.plot(x_data_x, y_data_x, color=color_x)
            if load_type_x == 'cyclic':
                ax2_x.plot(indices, x_data_x, color=color_x)

    # Add labels and grid
    ax1_x.set_xlabel(xlabel_x)
    ax1_x.set_ylabel(ylabel_x)
    ax2_x.set_xlabel("Index")
    ax2_x.set_ylabel(xlabel_x)
    if grid_x:
        ax1_x.grid(True)
        ax2_x.grid(True)

    # Automatically scale the axes limits based on the data
    ax1_x.relim()
    ax1_x.autoscale()
    ax2_x.relim()
    ax2_x.autoscale()

    # Show legend
    ax1_x.legend()
    ax2_x.legend()
    

# %%% TODO [02-01] PLOT INDEX VS STRAIN
def plot_index_strain_video(data_array_x, start_value, color_x, label_x, xlabel_x, ylabel_x, grid_x, load_type_x, line_width, ax_x=None):
    # If no axes object is provided, create a new figure with the specified size and resolution
    if ax_x is None:
        fig_x = plt.figure(figsize=(11, 3.2), dpi=100)

        cx_1 = 0.0725
        wx_1 = 0.4025
        cx_2 = 0.5765
        wx_2 = 0.4025
        ax1_x = fig_x.add_axes([cx_1, 0.133, wx_1, 0.827])
        ax2_x = fig_x.add_axes([cx_2, 0.133, wx_2, 0.827])

    else:
        ax1_x, ax2_x = ax_x

    # PLOT AX1 ################################################################
    # Determine the number of plots based on the number of columns
    num_columns_x = data_array_x.shape[1]
    num_plots_x = num_columns_x // 2

    # Plot each pair of columns
    for i in range(num_plots_x):
        x_data_x = data_array_x[:, 2 * i]
        # Assuming start_value is the value from which you want to start the indices
        indices = np.arange(start=start_value, stop=start_value + x_data_x.size)
        y_data_x = data_array_x[:, 2 * i + 1]
        if i == 0:
            # In case that label_x is None, don't show the label
            if label_x is not None:
                ax1_x.plot(x_data_x, y_data_x, color=color_x, label=label_x, lw=line_width)
            else:
                ax1_x.plot(x_data_x, y_data_x, color=color_x, lw=line_width)
            if load_type_x == 'cyclic':
                # In case that label_x is None, don't show the label
                if label_x is not None:
                    ax2_x.plot(indices, x_data_x, color=color_x, label=label_x, lw=line_width)
                else:
                    ax2_x.plot(indices, x_data_x, color=color_x, lw=line_width)
                    
        else:
            ax1_x.plot(x_data_x, y_data_x, color=color_x, lw=line_width)
            if load_type_x == 'cyclic':
                ax2_x.plot(indices, x_data_x, color=color_x, lw=line_width)

    # Add labels and grid
    ax1_x.set_xlabel(xlabel_x)
    ax1_x.set_ylabel(ylabel_x)
    ax2_x.set_xlabel("Index")
    ax2_x.set_ylabel(xlabel_x)
    if grid_x:
        ax1_x.grid(True)
        ax2_x.grid(True)

    # Automatically scale the axes limits based on the data
    ax1_x.relim()
    ax1_x.autoscale()
    ax2_x.relim()
    ax2_x.autoscale()

    # Show legend
    ax1_x.legend()
    ax2_x.legend()


# %%% TODO [02-01] PLOT INDEX VS STRAIN
def plot_index_strain_only(list_strain, color_x, label_x, grid_x, ax_x=None):
    # If no axes object is provided, create a new figure with the specified size and resolution
    if ax_x is None:
        fig_x = plt.figure(figsize=(5.5, 3.2), dpi=100)
        ax_x = fig_x.add_axes([0.145, 0.133, 0.805, 0.827])

    # Create indices
    indices = np.arange(len(list_strain))
    
    # Plot the strain data located in list_strain
    ax_x.plot(indices, list_strain, color=color_x, label=label_x, marker='o', linestyle='', markersize=2)

    # Add labels and grid
    ax_x.set_xlabel("Index")
    ax_x.set_ylabel('Strain [-]')
    if grid_x:
        ax_x.grid(True)

    # Automatically scale the axes limits based on the data
    ax_x.relim()
    ax_x.autoscale()

    # Show legend
    ax_x.legend()


# %% [03] TEST FUNCTIONS

# %%% [03-00] plot_strain_stress()
# Run only if it is the main file.
if __name__ == '__main__':
    import S01_GUI02_A02_fileText as TxT

    # Create figure
    figsize = (5.5, 3.2)
    dpi = 100
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_axes([0.145, 0.133, 0.805, 0.827])

    # Read the .txt files
    URL = r"C_GUI02_uniaxialMaterial\cyclic_compression/MatTag_1.txt"

    # Reads the contents of the file
    data_dict = TxT.read_file_to_dict(URL)

    # Unified unit
    unit_factors_new = {
        'kgf/cm**2': {'kgf/cm**2': 1, 'tonf/m**2': 0.1, 'ksi': 70.3069579639159, 'psi': 0.070306957963916,
                      'Pa': 0.00001019716213, 'MPa': 10.1971621297793},
        'tonf/m**2': {'kgf/cm**2': 10, 'tonf/m**2': 1, 'ksi': 703.069579639159, 'psi': 0.703069579639159,
                      'Pa': 0.000101971621298, 'MPa': 101.971621297793},
        'ksi': {'kgf/cm**2': 0.014223343307, 'tonf/m**2': 0.0014223343307, 'ksi': 1, 'psi': 0.001,
                'Pa': 0.000000145037738, 'MPa': 0.145037737730209},
        'psi': {'kgf/cm**2': 14.223343307, 'tonf/m**2': 1.4223343307, 'ksi': 1000, 'psi': 1, 'Pa': 0.000145037737730,
                'MPa': 145.037737730209},
        'Pa': {'kgf/cm**2': 98066.5, 'tonf/m**2': 9806.65, 'ksi': 6894757.29316836, 'psi': 6894.75729316836, 'Pa': 1,
               'MPa': 1000000},
        'MPa': {'kgf/cm**2': 0.0980665, 'tonf/m**2': 0.00980665, 'ksi': 6.89475729316836, 'psi': 0.00689475729316836,
                'Pa': 0.000001, 'MPa': 1}
    }
    # graphic_unit = graphic_unit_dropdown.value
    graphic_unit = ['kgf/cm**2', 'tonf/m**2', 'ksi', 'psi', 'Pa', 'MPa']
    graphic_unit = graphic_unit[0]
    # unit = graphic_unit_dropdown.value
    unit = ['kgf/cm**2', 'tonf/m**2', 'ksi', 'psi', 'Pa', 'MPa']
    unit = unit[0]

    # Convert stress values to the selected unit
    data_list = data_dict['DataPlot']
    data_array = np.array(data_list, dtype=np.float64)
    # Determine the number of plots based on the number of columns
    num_columns = data_array.shape[1]
    num_plots = num_columns // 2
    # Apply the conversion factor to each stress column
    for k in range(num_plots):
        x_data = data_array[:, 2 * k]
        y_data = data_array[:, 2 * k + 1] * unit_factors_new[graphic_unit][unit]
    data_array = np.column_stack((x_data, y_data))

    # Define graphic properties 
    colors = ['b', 'r', 'g', 'k', 'orange', 'm', 'purple', 'pink', 'brown', 'gray', 'olive', 'cyan', 'magenta', 'lime',
              'y', 'indigo', 'c', 'gold', 'teal', 'navy']
    color = colors[0]
    label = data_dict['model']
    xlabel, ylabel = 'strain', f'stress [{unit}]'
    grid = True

    # Graphic
    plot_strain_stress(data_array, color, label, xlabel, ylabel, grid, ax)

    # Invert both axes
    ax.invert_xaxis()
    ax.invert_yaxis()

    URL_img = 'C_GUI02_uniaxialMaterial/imagen.png'
    plt.savefig(URL_img)


# %%% [03-01] plot_index_strain()
# Run only if it is the main file.
if __name__ == '__main__':
    import S01_GUI02_A02_fileText as TxT

    # Create figure
    fig = plt.figure(figsize=(11, 3.2), dpi=100)
    ax1 = fig.add_axes([0.0725, 0.133, 0.4025, 0.827])
    ax2 = fig.add_axes([0.5765, 0.133, 0.4025, 0.827])
    ax = (ax1, ax2)

    # Read the .txt files
    URL = r"C_GUI02_uniaxialMaterial\cyclic_compression/MatTag_1.txt"
    # Reads the contents of the file
    data_dict = TxT.read_file_to_dict(URL)

    # Unified unit
    unit_factors_new = {
        'kgf/cm**2': {'kgf/cm**2': 1, 'tonf/m**2': 0.1, 'ksi': 70.3069579639159, 'psi': 0.070306957963916,
                      'Pa': 0.00001019716213, 'MPa': 10.1971621297793},
        'tonf/m**2': {'kgf/cm**2': 10, 'tonf/m**2': 1, 'ksi': 703.069579639159, 'psi': 0.703069579639159,
                      'Pa': 0.000101971621298, 'MPa': 101.971621297793},
        'ksi': {'kgf/cm**2': 0.014223343307, 'tonf/m**2': 0.0014223343307, 'ksi': 1, 'psi': 0.001,
                'Pa': 0.000000145037738, 'MPa': 0.145037737730209},
        'psi': {'kgf/cm**2': 14.223343307, 'tonf/m**2': 1.4223343307, 'ksi': 1000, 'psi': 1, 'Pa': 0.000145037737730,
                'MPa': 145.037737730209},
        'Pa': {'kgf/cm**2': 98066.5, 'tonf/m**2': 9806.65, 'ksi': 6894757.29316836, 'psi': 6894.75729316836, 'Pa': 1,
               'MPa': 1000000},
        'MPa': {'kgf/cm**2': 0.0980665, 'tonf/m**2': 0.00980665, 'ksi': 6.89475729316836, 'psi': 0.00689475729316836,
                'Pa': 0.000001, 'MPa': 1}
    }
    # graphic_unit = graphic_unit_dropdown.value
    graphic_unit = ['kgf/cm**2', 'tonf/m**2', 'ksi', 'psi', 'Pa', 'MPa']
    graphic_unit = graphic_unit[0]
    # unit = graphic_unit_dropdown.value
    unit = ['kgf/cm**2', 'tonf/m**2', 'ksi', 'psi', 'Pa', 'MPa']
    unit = unit[1]

    # Convert stress values to the selected unit
    data_list = data_dict['DataPlot']
    data_array = np.array(data_list, dtype=np.float64)
    # Determine the number of plots based on the number of columns
    num_columns = data_array.shape[1]
    num_plots = num_columns // 2
    # Apply the conversion factor to each stress column
    for k in range(num_plots):
        x_data = data_array[:, 2 * k]
        y_data = data_array[:, 2 * k + 1] * unit_factors_new[graphic_unit][unit]
    data_array = np.column_stack((x_data, y_data))

    # Define graphic properties 
    colors = ['b', 'r', 'g', 'k', 'orange', 'm', 'purple', 'pink', 'brown', 'gray', 'olive', 'cyan', 'magenta', 'lime',
              'y', 'indigo', 'c', 'gold', 'teal', 'navy']
    color = colors[0]
    label = data_dict['model']
    xlabel, ylabel = 'strain', f'stress [{unit}]'
    grid = True

    # Graphic
    plot_index_strain(data_array, color, label, xlabel, ylabel, grid, ax)

    # Invert both axes
    ax1.invert_xaxis()
    ax1.invert_yaxis()
    ax2.invert_yaxis()

    URL_img = 'C_GUI02_uniaxialMaterial/imagen2.png'
    plt.savefig(URL_img)
