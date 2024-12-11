# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-06-12
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI02_A05_CallGraphic.py
COMENTARIOS:    Define material a testear en openseespy.
"""

# %%  [00] INTRODUCTION
# Para graficar diferentes curvas esfuerzo deformación en un mismo gráfico, es necesario repetir estas líneas de código
# para cada curva. Por lo tanto, se ejecutarán estas líneas de código desde este script, en atención a extensión original
# del código.


# %%  [01] CODE
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

colors = ['b', 'r', 'g', 'k', 'orange', 'm', 'purple', 'pink', 'brown', 'gray', 'olive', 'cyan', 'magenta', 'lime',
          'y', 'indigo', 'c', 'gold', 'teal', 'navy']

graphic_unit = graphic_unit_dropdown.value
id_mat_tag = []
data_dict = {}
for index, url in enumerate(selected_files):
    # This conditional is for fast running. Avoid to write a txt file with the data
    # of the model that is already modifying using the GUI.
    # Only graph the data from a txt file if the url is different from 'Dictionary_with_direct_data'.
    if url == 'Dictionary_with_direct_data':
        data_dict = dictionary  # Dictionary defined using the parameters of actual GUI
    else:
        url_x = f"{url}"
        # Reads the contents of the file
        data_dict = TxT.read_file_to_dict(url_x)
    
    unit = data_dict['unit']

    # Convert stress values to the selected unit
    data_list = data_dict['DataPlot']
    data_array = np.array(data_list, dtype=np.float64)
    # Determine the number of plots based on the number of columns
    num_columns = data_array.shape[1]
    num_plots = num_columns // 2

    # Create an empty list to store all the data
    all_data = []
    # Apply the conversion factor to each stress column
    for k in range(num_plots):
        x_data = data_array[:, 2 * k]
        # If both are adimensional values, there isn't problem.
        if unit == "-" and graphic_unit == "-":
            y_data = data_array[:, 2 * k + 1]
        # If one of them is adimensional and the other is not, raise an exception.
        if unit == "-" and graphic_unit != "-":
            graph_output.value = "The selected graphic unit is not adimensional."
            code_params_output.value = ""
            raise Exception("The selected graphic unit is not adimensional.")
        if unit != "-" and graphic_unit == "-":
            graph_output.value = "The selected graphic unit is not dimensional."
            code_params_output.value = ""
            raise Exception("The selected graphic unit is not dimensional.")
        # If both are dimensional values, apply the conversion factor.
        if unit != "-" and graphic_unit != "-":
            y_data = data_array[:, 2 * k + 1] * unit_factors_new[graphic_unit][unit]
        # Append the x_data and y_data to the all_data list
        all_data.append(x_data)
        all_data.append(y_data)
    # Stack all the data together
    data_array = np.column_stack(all_data)

    # Define graphic properties
    color = colors[index]
    label = data_dict['model']

    xlabel, ylabel = 'strain', f'stress [{graphic_unit}]'
    grid = True

    # Graphic.
    if aux_ax == 1:
        Grf.plot_strain_stress(data_array, color, label, xlabel, ylabel, grid, ax)
    elif aux_ax == 2:
        Grf.plot_index_strain(data_array, color, label, xlabel, ylabel, grid, data_dict['load_type'], ax)
    elif aux_ax == 3:
        if data_dict['load_type'] != 'cyclic':
            graph_output.value = "The load type is not cyclic."
            code_params_output.value = ""
                    
            # Enable initial widgets
            for widget in all_buttons_and_widgets_list:
                if widget in buttons_initial_state:
                    widget.disabled = False
                else:
                    widget.disabled = True
            instructions_button.disabled = False
            
            raise Exception("The load type is not cyclic.")
        
        # Colors of the curves.
        color_grey_rgba = (130/255, 130/255, 130/255, 1)
        color_blue_rgba = (0/255, 0/255, 255/255, 1)
        
        # Line width of the curves.
        line_width_thin = 1.0
        line_width_thick = 2.25
        
        # To stop the graphic when the strain is 0, I'm going to make mutiples frames (15) 
        # for the values where the strain is 0.
        # Find indices where the strain (first column) is exactly 0
        zero_indices = np.where(data_array[:, 0] == 0.0)[0]
        
        # aux_zero_indices = 1  # Auxiliar to plot more than one frame for zero values. 
        
        # Make a video. Take a for cycle that iterates over the data_array and plot each curves.
        step_frames = 3  # Adjust the numbers of rows that involve a frame.
        id_image = 0  # Counter for the image name.
        for i in range(0, data_array.shape[0], step_frames):
            # Calculate the index of the last zero value before i
            aux_zero_indices = len(np.where(zero_indices < i)[0])
            
            graph_output.value = f'Making frames: {i} of {data_array.shape[0]} frames.'
            
            if i >= (zero_indices[aux_zero_indices] - int(step_frames-1)) and \
            i < (zero_indices[aux_zero_indices] + int(step_frames-1)) and \
                aux_zero_indices != 0:
                    
                
                if aux_zero_indices == 1 or aux_zero_indices == 2:
                    fin_ciclo_activo = zero_indices[aux_zero_indices] +1
                    fin_ciclos_inactivos = zero_indices[aux_zero_indices-1]
                    fin_ciclos_inactivos_b = fin_ciclos_inactivos + 1
                    
                else:
                    fin_ciclo_activo = zero_indices[aux_zero_indices] +1
                    fin_ciclos_inactivos = zero_indices[aux_zero_indices-1]
                    fin_ciclos_inactivos_b = fin_ciclos_inactivos + 1
                    fin_ciclos_inactivos_2 = zero_indices[aux_zero_indices-2]
                    fin_ciclos_inactivos_2_b = fin_ciclos_inactivos_2 + 1
                
                num_frames_zero = 15   # 15 number of FPS to stop one second in video.
                for t in range(num_frames_zero):
                    code_params_output.value = f'Making frames in zero: {t} of {num_frames_zero-1} frames'
                    
                    # Color in the graphic is transitioned from blue to grey.
                    # t_color is the index of the color transition. It's intended to make faster the transition between colors.
                    t_color = t + 8
                    if t_color < num_frames_zero-1:
                        color_transition = (color_blue_rgba[0] - (color_blue_rgba[0] - color_grey_rgba[0]) * t_color / (num_frames_zero-1),
                                            color_blue_rgba[1] - (color_blue_rgba[1] - color_grey_rgba[1]) * t_color / (num_frames_zero-1),
                                            color_blue_rgba[2] - (color_blue_rgba[2] - color_grey_rgba[2]) * t_color / (num_frames_zero-1),
                                            1)
                    else:
                        color_transition = color_grey_rgba
                    
                    # Line width in the graphic is transitioned from thick to thin.
                    # t_line is the index of the line width transition. It's intended to make faster the transition between line widths.
                    t_line = t + 8
                    if t_line < num_frames_zero-1:
                        line_width_transition = line_width_thick - (line_width_thick - line_width_thin) * t_line / (num_frames_zero-1)
                    else:
                        line_width_transition = line_width_thin
                    
                    ax1.clear()
                    ax2.clear()
                    
                    if aux_zero_indices == 1 or aux_zero_indices == 2:
                        data_array_first_part = data_array[:fin_ciclos_inactivos_b, :]
                        data_array_second_part = data_array[fin_ciclos_inactivos:fin_ciclo_activo, :]
                        Grf.plot_index_strain_video(data_array_first_part, 0, color_grey_rgba, None, xlabel, ylabel, grid, data_dict['load_type'], line_width_thin, ax)
                        Grf.plot_index_strain_video(data_array_second_part, fin_ciclos_inactivos, color_transition, label, xlabel, ylabel, grid, data_dict['load_type'], line_width_transition, ax)
                        
                    else:
                        data_array_first_part = data_array[:fin_ciclos_inactivos_2_b, :]
                        data_array_second_part = data_array[fin_ciclos_inactivos_2:fin_ciclos_inactivos_b, :]
                        data_array_third_part = data_array[fin_ciclos_inactivos:fin_ciclo_activo, :]

                        Grf.plot_index_strain_video(data_array_first_part, 0, color_grey_rgba, None, xlabel, ylabel, grid, data_dict['load_type'], line_width_thin, ax)
                        Grf.plot_index_strain_video(data_array_second_part, fin_ciclos_inactivos_2, color_grey_rgba, None, xlabel, ylabel, grid, data_dict['load_type'], line_width_thin, ax)
                        Grf.plot_index_strain_video(data_array_third_part, fin_ciclos_inactivos, color_transition, label, xlabel, ylabel, grid, data_dict['load_type'], line_width_transition, ax)
                        
                    ax1.invert_xaxis()
                    ax1.invert_yaxis()
                    ax2.invert_yaxis()
                    # Save each plot as a .png file, into a directory named as the material tag.
                    plt.savefig(f'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/Fotogramas_Video/ID_{id_image:07}.png')
                    id_image += 1
                    
                code_params_output.value = ''
                
            else:
                fin_ciclos_inactivos = zero_indices[aux_zero_indices-1]
                fin_ciclos_inactivos_b = fin_ciclos_inactivos + 1
                
                if fin_ciclos_inactivos != i:
                    data_array_first_part = data_array[:fin_ciclos_inactivos_b, :]
                    data_array_second_part = data_array[fin_ciclos_inactivos:i, :]
                    ax1.clear()
                    ax2.clear()
                    Grf.plot_index_strain_video(data_array_first_part, 0, color_grey_rgba, None, xlabel, ylabel, grid, data_dict['load_type'], line_width_thin, ax)
                    Grf.plot_index_strain_video(data_array_second_part, fin_ciclos_inactivos, color_blue_rgba, label, xlabel, ylabel, grid, data_dict['load_type'], line_width_thick, ax)
                    
                    ax1.invert_xaxis()
                    ax1.invert_yaxis()
                    ax2.invert_yaxis()
                    # Save each plot as a .png file, into a directory named as the material tag.
                    plt.savefig(f'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/Fotogramas_Video/ID_{id_image:07}.png')
                    id_image += 1
        
        # Create the video.
        graph_output.value = f'Making video.'
        # Create a video with all the .png files.
        Vid.video('C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/Fotogramas_Video', 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/Cyclic_Video.mp4', 15)
        plt.close()
    id_mat_tag.append(data_dict['material']['matTag'])

url = r'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/img_MatTag'
for i in id_mat_tag:
    url = url + '_' + str(i)
url = url + '_' + data_dict['load_type'] + '_' + data_dict['cyclic_type'] + '.png'
# Annotation
graph_output.value = str(url)

# Invert axes
if aux_ax == 1:
    ax.invert_xaxis()
    ax.invert_yaxis()
elif aux_ax == 2:
    ax1.invert_xaxis()
    ax1.invert_yaxis()
    ax2.invert_yaxis()

# Save
plt.savefig(url)
plt.close()

if aux_ax == 1 or aux_ax == 2:
    # Display the image
    with out:
        display(Image(filename=url))

elif aux_ax == 3:
    # Display the video
    with out:
        display(Video('C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/Cyclic_Video.mp4', embed=True))