# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-06-08
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI02_A01_uniaxialMaterial.py
COMENTARIOS:    Interfaz grafica de usuario para definicion de UniaxialMaterial. 
"""

# %% [00] INTRODUCTION
# GUI in Jupyter Notebook that generate graphical representation of stress-strain curve of uniaxial materials.


# %% [01] LIBRARIES
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import HBox, VBox, Dropdown, IntText, Textarea, Output, Text
from IPython.display import display, Image, Video
import os
import shutil
import numpy as np
import urllib.parse
from typing import Optional
import matplotlib.patches as patches
import inspect

import sys
sys.path.insert(0, './C_GUI02_uniaxialMaterial')
import S01_GUI02_A02_2_fileText as TxT    
import S01_GUI02_A03_Graphic as Grf
import S01_GUI02_A07_UserDefFunIndications as Ind
import S01_GUI02_A08_Video as Vid


# %% [02] INITIALIZATION
# Activate the observer for all the interactive widgets and dropdowns
# This boolean variable is useful to update the parameters in the widgets 
# without create the same plot each time a value is changed.
observer_enabled = True

# Units for regularization
description_units = {
'kgf/cm**2': {'Unit fc_reg_input': 'kgf/cm**2', 'Unit Ec_reg_input': 'kgf/cm**2', 'Unit fr_reg_input': 'kgf/cm**2', 'Unit Gfc_cc_input': 'kgf/cm', 'Unit L_reg_input': 'cm'},
'tonf/m**2': {'Unit fc_reg_input': 'tonf/m**2', 'Unit Ec_reg_input': 'tonf/m**2', 'Unit fr_reg_input': 'tonf/m**2', 'Unit Gfc_cc_input': 'tonf/m', 'Unit L_reg_input': 'm'},
'ksi': {'Unit fc_reg_input': 'ksi', 'Unit Ec_reg_input': 'ksi', 'Unit fr_reg_input': 'ksi', 'Unit Gfc_cc_input': 'kip/IN', 'Unit L_reg_input': 'IN'},
'psi': {'Unit fc_reg_input': 'psi', 'Unit Ec_reg_input': 'psi', 'Unit fr_reg_input': 'psi', 'Unit Gfc_cc_input': 'lbf/IN', 'Unit L_reg_input': 'IN'},
'Pa': {'Unit fc_reg_input': 'Pa', 'Unit Ec_reg_input': 'Pa', 'Unit fr_reg_input': 'Pa', 'Unit Gfc_cc_input': 'N/m', 'Unit L_reg_input': 'm'},
'MPa': {'Unit fc_reg_input': 'MPa', 'Unit Ec_reg_input': 'MPa', 'Unit fr_reg_input': 'MPa', 'Unit Gfc_cc_input': 'N/mm', 'Unit L_reg_input': 'mm'},
}

# Convertion of units: Stress
unit_factors_new = {
'kgf/cm**2': {'kgf/cm**2': 1, 'tonf/m**2': 0.1, 'ksi': 70.3069579639159, 'psi': 0.070306957963916,
                'Pa': 0.00001019716213, 'MPa': 10.1971621297793},
'tonf/m**2': {'kgf/cm**2': 10, 'tonf/m**2': 1, 'ksi': 703.069579639159, 'psi': 0.703069579639159,
                'Pa': 0.000101971621298, 'MPa': 101.971621297793},
'ksi': {'kgf/cm**2': 0.014223343307, 'tonf/m**2': 0.0014223343307, 'ksi': 1, 'psi': 0.001,
        'Pa': 0.000000145037738, 'MPa': 0.145037737730209},
'psi': {'kgf/cm**2': 14.223343307, 'tonf/m**2': 1.4223343307, 'ksi': 1000, 'psi': 1,
        'Pa': 0.000145037737730,
        'MPa': 145.037737730209},
'Pa': {'kgf/cm**2': 98066.5, 'tonf/m**2': 9806.65, 'ksi': 6894757.29316836, 'psi': 6894.75729316836,
        'Pa': 1,
        'MPa': 1000000},
'MPa': {'kgf/cm**2': 0.0980665, 'tonf/m**2': 0.00980665, 'ksi': 6.89475729316836,
        'psi': 0.00689475729316836,
        'Pa': 0.000001, 'MPa': 1}
}

# Convertion of units: Force/Length
unit_factors_new_2 = {
'kgf/cm': {'kgf/cm': 1, 'tonf/m': 10, 'kip/IN': 178.579673228346, 'lbf/IN': 0.178579673228346,
            'N/m': 0.001019716212978, 'N/mm': 1.01971621297793},
'tonf/m': {'kgf/cm': 0.1, 'tonf/m': 1, 'kip/IN': 17.8579673228346, 'lbf/IN': 0.017857967322835,
                'N/m': 0.000101971621298, 'N/mm': 0.101971621297793},
'kip/IN': {'kgf/cm': 0.005599741459496, 'tonf/m': 0.055997414594959, 'kip/IN': 1, 'lbf/IN': 0.001,
            'N/m': 0.000005710147155, 'N/mm': 0.005710147154733},
'lbf/IN': {'kgf/cm': 5.59974145949589, 'tonf/m': 55.9974145949589, 'kip/IN': 1000, 'lbf/IN': 1,
            'N/m': 0.005710147154733, 'N/mm': 5.71014715473265},
'N/m': {'kgf/cm': 980.665, 'tonf/m': 9806.65, 'kip/IN': 175126.835246476,
        'lbf/IN': 175.126835246476, 'N/m': 1, 'N/mm': 1000},
'N/mm': {'kgf/cm':0.980665, 'tonf/m': 9.80665, 'kip/IN': 175.126835246476, 'lbf/IN': 0.175126835246476,
            'N/m': 0.001, 'N/mm': 1}
}

# Convertion of units: Length
unit_factors_new_3 = {
'cm': {'cm': 1, 'm': 100, 'IN': 2.54, 'mm': 0.1},
'm': {'cm': 0.01, 'm': 1, 'IN': 0.0254, 'mm': 0.001},
'IN': {'cm': 0.393700787401575, 'm': 39.3700787401575, 'IN': 1, 'mm': 0.0393700787401575},
'mm': {'cm': 10, 'm': 1000, 'IN': 25.4, 'mm': 1}
}

# Create directories for the GUI in case it doesn't exist.
def create_directory(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


# Directories to create
directories = ['C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial',
               'C_GUI02_uniaxialMaterial/C_GUI02_StrainLoad',
               'C_GUI02_uniaxialMaterial/C_GUI02_MaterialModel',
               'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/monotonic',
               'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/cyclic_traction',
               'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/cyclic_compression',
               'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/cyclic_combined',
               'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/Fotogramas_Video']

# Create all directories
for dir_i in directories:
    create_directory(dir_i)


# %% [03] FUNCTIONS
#
# %%% [03-00] UPDATE DROPDOWNS
#
# Function to update the "Unit" dropdown based on "Graphic Unit"
def update_unit_options(change=None):
    if graphic_unit_dropdown.value == '-':
        unit_dropdown.options = ['-']
        unit_dropdown.disabled = True
    else:
        unit_dropdown.disabled = False
        unit_dropdown.options = ['kgf/cm**2', 'tonf/m**2', 'ksi', 'psi', 'Pa', 'MPa']
    update_model_widgets()


# Function to update the type dropdown based on material type
def update_model_type_dropdown(change=None):
    if material_type_dropdown.value == 'Concrete':
        model_type_dropdown.options = ['ConcreteCM', 'Concrete07']
        model_type_dropdown.value = 'ConcreteCM'
    elif material_type_dropdown.value == 'Steel':
        model_type_dropdown.options = ['Steel01', 'Steel02', 'Steel4', 'SteelMPF']
        model_type_dropdown.value = 'SteelMPF'
    elif material_type_dropdown.value == 'MinMax':
        model_type_dropdown.options = ['-']
        model_type_dropdown.value = '-'
    elif material_type_dropdown.value == 'User defined':
        model_type_dropdown.options = ['Saatcioglu(1992)', 'Mander(1988)', 'Belarbi(1994)']
        model_type_dropdown.value = 'Saatcioglu(1992)'
        #load_type_dropdown.value = 'monotonic'
    update_model_widgets()


# Function to update the type dropdown based on material type
def update_cyclic_type_dropdown(change=None):
    if load_type_dropdown.value == 'monotonic':
        cyclic_type_dropdown.options = ['-']
        cyclic_type_dropdown.disabled = True
    elif load_type_dropdown.value == 'cyclic':
        cyclic_type_dropdown.disabled = False
        cyclic_type_dropdown.options = ['compression', 'combined', 'traction']
        cyclic_type_dropdown.value = 'compression'
    update_defo_widgets()


# %%% [03-01] INPUT DATA
#
# Function to update model_widgets layout based on model type
def update_model_widgets(change=None):
    regularization_concrete = False  # Flag to activate the regularization of the concrete model parameters
    
    text_model_param = widgets.HTML(value="Model Parameters: ")
    text_model_param.style.font_size = '14px'
    material_type = material_type_dropdown.value
    model_type = model_type_dropdown.value
    unit = unit_dropdown.value
    new_widgets = []

    def update_description(widget_x, desc, unit_x=unit):
        if unit_x != '-':
            if unit_x == 'kgf/cm**2':
                unit_x = 'kgf/cm'
                widget_x.description = f"{desc} [{unit_x}\u00b2]"
            elif unit_x == 'tonf/m**2':
                unit_x = 'tonf/m'
                widget_x.description = f"{desc} [{unit_x}\u00b2]"
            elif unit_x == 'N/mm**2':
                unit_x = 'N/mm'
                widget_x.description = f"{desc} [{unit_x}\u00b2]"
            else:
                widget_x.description = f"{desc} [{unit_x}]"
        else:
            widget_x.description = desc


    if model_type == 'ConcreteCM':
        new_widgets = [fpcc_input, epcc_input, Ec_input, rc_input, xcrn_input, ft_input, et_input, rt_input,
                        xcrp_input, GapClose_dropdown, GapClose_input]
        update_description(fpcc_input, "fpcc:")
        update_description(Ec_input, "Ec:")
        update_description(ft_input, "ft:")
        # Bellow the widgets of the model is situated the regularization of the model parameters.
        if material_type == 'Concrete':
            regularization_concrete = True
            
    elif model_type == 'Concrete07':
        new_widgets = [fc_input, epsc_input, Ec_input, ft_input, et_input, xp_input, xn_input, r_input]
        update_description(fc_input, "fc:")
        update_description(Ec_input, "Ec:")
        update_description(ft_input, "ft:")
        # Bellow the widgets of the model is situated the regularization of the model parameters.
        if material_type == 'Concrete':
            regularization_concrete = True
            
    elif model_type == 'SteelMPF':
        new_widgets = [fyp_input, fyn_input, E0_input, bp_input, bn_input, R0_input, cR1_input, cR2_input, a1_input,
                        a2_input, a3_input, a4_input]
        update_description(fyp_input, "fyp:")
        update_description(fyn_input, "fyn:")
        update_description(E0_input, "E0:")
    
    elif model_type == 'Steel02':
        new_widgets = [Fy_Steel02_input, E0_Steel02_input, b_Steel02_input, R0_Steel02_input, cR1_Steel02_input, cR2_Steel02_input,
                        a1_Steel02_input, a2_Steel02_input, a3_Steel02_input, a4_Steel02_input, sigInit_Steel02_input]
        update_description(Fy_Steel02_input, "Fy:")
        update_description(E0_Steel02_input, "E0:")
    
    elif model_type == 'Steel01':
        new_widgets = [Fy_Steel01_input, E0_Steel01_input, b_Steel01_input, 
                       a1_Steel01_input, a2_Steel01_input, a3_Steel01_input, a4_Steel01_input]
        update_description(Fy_Steel01_input, "Fy:")
        update_description(E0_Steel01_input, "E0:")
    
    elif model_type == 'Steel4':
        new_widgets = [Fy_Steel4_input, E0_Steel4_input, b_k_Steel4_input, R0_Steel4_input, r1_Steel4_input, r2_Steel4_input,
                       b_kc_Steel4_input, R0c_Steel4_input, r1c_Steel4_input, r2c_Steel4_input,
                       b_i_Steel4_input, rho_i_Steel4_input, b_I_Steel4_input, R_i_Steel4_input,
                       I_yp_Steel4_input, b_ic_Steel4_input, rho_ic_Steel4_input, b_Ic_Steel4_input, R_ic_Steel4_input,
                       f_u_Steel4_input, R_u_Steel4_input, f_uc_Steel4_input, R_uc_Steel4_input,
                       sig_init_Steel4_input, cycNum_Steel4_input]
        update_description(Fy_Steel4_input, "Fy:")
        update_description(E0_Steel4_input, "E0:")
        update_description(f_u_Steel4_input, "fu:")
        update_description(f_uc_Steel4_input, "fuc:")

    elif model_type == 'Saatcioglu(1992)':
        new_widgets = [see_instruction_button, fco_input, fl_input, e01_input, rho_input, e085_input]
        update_description(fco_input, "fco:", unit)
        update_description(fl_input, "fle:", unit)

    elif model_type == 'Mander(1988)':
        new_widgets = [see_instruction_button, fco_input, CSR_input, eco_input, Ec_input]
        update_description(fco_input, "fco:", unit)
        update_description(Ec_input, "Ec:")
        
    elif model_type == 'Belarbi(1994)':
        new_widgets = [see_instruction_button, f_cr_input, eps_cr_input, Ecr_input]
        update_description(f_cr_input, "fcr:", unit)
        update_description(Ecr_input, "Ecr:", unit)

    
    if len(new_widgets) == 0:
        model_widgets.children = []
    else:
        model_widgets.children = [text_model_param] + new_widgets
    
    model_type_dropdown.disabled = False
    MatTag_input.disabled = False
    
    if regularization_concrete:
        # Add the regularization parameters for the model
        if unit != '-':
            global description_units
            reg_widgets = [regularization_button, fc_reg_input, ec_reg_input, Ec_reg_input, fr_reg_input, Gfc_cc_input, L_reg_input]
            update_description(fc_reg_input, "fc:", description_units[unit]['Unit fc_reg_input'])
            update_description(Ec_reg_input, "Ec:", description_units[unit]['Unit Ec_reg_input'])
            update_description(fr_reg_input, "fr:", description_units[unit]['Unit fr_reg_input'])
            update_description(Gfc_cc_input, "Gf:", description_units[unit]['Unit Gfc_cc_input'])
            update_description(L_reg_input, "L:", description_units[unit]['Unit L_reg_input'])
            regularization_widgets.children = reg_widgets
    else:
        regularization_widgets.children = []
    
    if material_type == 'MinMax':
        text_minmax_param = widgets.HTML(value="MinMax Parameters: ")
        text_minmax_param.style.font_size = '14px'
        min_max_widgets = [MatTag_minmax_input, OtherTag_minmax_dropdown, minStrain_input, maxStrain_input, MinMax_button]
        regularization_widgets.children = [text_minmax_param] + min_max_widgets
        model_type_dropdown.disabled = True
        MatTag_input.disabled = True
    
    # Enable all Text widgets within the VBox
    for widget in model_widgets.children:
        if isinstance(widget, Text):
            widget.disabled = False
    
    
# Function to update defo_widgets layout based on model type
def update_defo_widgets(change=None):
    text_cyclic_defo = widgets.HTML(value="Strain Parameters: ")
    text_cyclic_defo.style.font_size = '14px'
    load_type = load_type_dropdown.value
    cyclic_type = cyclic_type_dropdown.value
    new_widgets = []
    if load_type == 'monotonic':
        new_widgets = [delta_e, e_max_c, e_max_t]
    elif load_type == 'cyclic':
        if cyclic_type == 'compression':
            new_widgets = [delta_e, e_max_c_1, pulso_1, e_max_c_2, pulso_2, e_max_c_3, pulso_3, e_max_c_4, pulso_4, e_max_c_5, pulso_5]
        elif cyclic_type == 'traction':
            new_widgets = [delta_e, e_max_t_1, pulso_1, e_max_t_2, pulso_2, e_max_t_3, pulso_3, e_max_t_4, pulso_4, e_max_t_5, pulso_5]
        elif cyclic_type == 'combined':
            new_widgets = [delta_e, e_max_c_1, e_max_t_1, pulso_1, e_max_c_2, e_max_t_2, pulso_2, e_max_c_3, e_max_t_3, pulso_3, 
                           e_max_c_4, e_max_t_4, pulso_4, e_max_c_5, e_max_t_5, pulso_5]
    model_widgets.children = [text_cyclic_defo] + new_widgets


# %%% [03-02] SELECT FILES (CHECKBOX)
# Function to list .txt files in a directory and create checkboxes
def list_files_with_checkboxes(directory_x: str) -> list:
    try:
        file_checkboxes = []
        for root, dirs, files in os.walk(directory_x):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, directory_x)
                    checkbox = widgets.Checkbox(value=False, description=relative_path, disabled=False,
                                                layout=widgets.Layout(width='387px', margin='0 0 0 -86px'))
                    file_checkboxes.append(checkbox)
        return file_checkboxes
    except Exception as e:
        code_params_output.value = "\nError: Check files in directory."
        return []


# %%% [03-03] ACTIONS WITH FILES (CHECKBOX)
# Function to display selected file. Function to try checkbox.
def display_selected_files(files):
    selected_files = [cb.description for cb in files if cb.value]
    # Action that you want with the checkbutton
    code_params_output.value = '\n'.join(selected_files)


# %%% [03-04] BUTTONS

# %%%% [03-04-00] SEE_USER_DEFINED_MATERIALS_INSTRUCTIONS
# Function to show the instructions of the user defined materials functions.
def see_instruction(change=None):
    material_type = material_type_dropdown.value
    model_type = model_type_dropdown.value
    if material_type == 'User defined':
        if model_type == 'Saatcioglu(1992)':
            code_params_output.value = Ind.instructions['Saatcioglu(1992)']
            graph_output.value = 'C_GUI02_uniaxialMaterial/S01_GUI02_A10_Saatcioglu(1992).png'
            with out:
                out.clear_output()
                display(Image(filename='C_GUI02_uniaxialMaterial/S01_GUI02_A10_Saatcioglu(1992).png'))
        elif model_type == 'Mander(1988)':
            code_params_output.value = Ind.instructions['Mander(1988)']
            graph_output.value = 'C_GUI02_uniaxialMaterial/S01_GUI02_A11_Mander(1988).png'
            with out:
                out.clear_output()
                display(Image(filename='C_GUI02_uniaxialMaterial/S01_GUI02_A11_Mander(1988).png'))
        elif model_type == 'Belarbi(1994)':
            code_params_output.value = Ind.instructions['Belarbi(1994)']
            graph_output.value = 'C_GUI02_uniaxialMaterial/S01_GUI02_A12_Belarbi(1994).png'
            with out:
                out.clear_output()
                display(Image(filename='C_GUI02_uniaxialMaterial/S01_GUI02_A12_Belarbi(1994).png'))


# %%%% [03-04-01] ADD_RESPONSE
# Explanation:
# The button "add_file_button" call the function "add_response" when it is clicked.
# The function "add_response" create a file with the material model and the result of test it.
# The function "add_response" call the function "create_responses_file" to create the responses file. 
# ---
# To call it, it identify an argument aux_checkbox. This argument is used to identify if 
# the strain loading is selected from the checkbox or from the dropdown.
# The function "read_selected_files_strain" is used to read the selected file in the strain loading dropdown
# or the default file. This function return the parameters of the strain loading.
# Example of content in file "C_GUI02_uniaxialMaterial/ID_StrainLoad_99_monotonic_-.txt", default strain loading:
#       monotonic
#       -
#       0.0001
#       -0.008
#       0
# ---
# To obtain the parameters of the model, the function "model_arg" is used.
# This function return a list model_args suitable to crate the file with the material model and its response.
# The args of this list are defined in accordance with the paramters needed in TxT.file_txt().
# ---
# To save the file the function "url_arg" is used. This function return the URL with 
# the directory to save the file. The ID_cyclic_strain is used to name the file created.
# ---
# Finally, the function "add_response" call the function "show_material_model" to 
# display the material model.

# Function to create responses file
def create_responses_file(selected_file_in_strain_dropdown, aux_checkbox = True):

    # Define the cyclic load arguments
    if aux_checkbox:
        load_args, ID_cyclic_strain = read_selected_files_strain(selected_file_in_strain_dropdown)
    else:
        load_args, ID_cyclic_strain = read_selected_files_strain(selected_file_in_strain_dropdown, aux_checkbox = False)
    
    # Define the URL to save the txt file
    load_type = load_args[0]
    cyclic_type = load_args[1]
    url_args = url_arg(load_type, cyclic_type)
    
    # Define the unit of the model
    unit = unit_dropdown.value
    
    # Define the material model arguments
    # There are two possible situations:
    # 1. The user define a MinMax material model.
    #    - This implies pass to the TxT.file_txt aditional arguments. 
    #    - The model_args of the original material, and the model args of the MinMax material.
    # 2. The user define a Concrete/Steel/User defined material model.
    #    - It implies only pass the default argument to the TxT.file_txt function.
    if material_type_dropdown.value == 'MinMax':
        model_args = model_arg()
        min_max_args = min_max_model_arg()
        
        # Made the third term of min_max_args a type int
        min_max_args[2] = int(min_max_args[2])
        
        # Create file
        TxT.file_txt(url_args, unit, model_args, load_args, ID_cyclic_strain, min_max_args_x = min_max_args)
        
    else:
        model_args = model_arg()
        # Create file
        TxT.file_txt(url_args, unit, model_args, load_args, ID_cyclic_strain)
    
    # Refresh Checkbox
    refresh_files()
    
    # Message
    mat_tag = model_args[1]
    url_doc = f"MatTag_{mat_tag}_IdStrainLoad_{ID_cyclic_strain}.txt"
    url_file = url_args + url_doc
    code_params_output.value = f"File '{url_file}' has been created successfully."


# Function to add a responses file
def add_response(change=None):
    global files_checkboxes_2, files_checkboxes_3, selected_strain_dropdown
    
    # Obtain the selected value of the strain loading dropdown
    selected_strain_dropdown = strain_loading_dropdown.value

    # If there aren't selected files, the code use default parameters
    if selected_strain_dropdown == '-':
        # Create the graphic with the default values
        selected_files = ['C_GUI02_uniaxialMaterial/ID_StrainLoad_99_monotonic_-.txt']
        
        # Create file with the material model and the result of test it
        # aux_checkbox = False is used to identify that the strain loading used is the default file.
        create_responses_file(selected_files, aux_checkbox = False)
        
    else:
        code_params_output.value = ''

        # Create a list with a unique value. This value is the file with the strain loading selected 
        # This is necessary to reutilize the function read_selected_files_strain
        selected_file_in_strain_dropdown = [cb for cb in files_checkboxes_2 if cb.description == selected_strain_dropdown]

        # Activate the checkbox of the selected value in the list, to use the function read_selected_files_strain
        selected_file_in_strain_dropdown[0].value = True
            
        # Create file with the material model and the result of test it
        create_responses_file(selected_file_in_strain_dropdown)

    show_material_model()


# %%%% [03-04-02] SHOW_GRAPHIC
# This function is called when the button "show_graphic_button" is clicked.
# Only graph the stress-strain curve of the selected files already saved as responses.

# Function to graphic stress-strain curve of selected files
def show_graphic(change=None):
    global files_checkboxes, directory
    graph_output.value = ""
    with out:
        out.clear_output()
    
    # Find the selected files with the responses
    selected_files = [cb.description for cb in files_checkboxes if cb.value]
    # Reformat URL to be consistence
    selected_files = [direc.replace('\\', '/') for direc in selected_files]
    selected_files = [f"{directory}/{direc}" for direc in selected_files]
    directory = directory.replace('/', '\\')
    
    # Create figure
    fig = plt.figure(figsize=(6.875, 4), dpi=100)
    ax = fig.add_axes([0.145, 0.133, 0.805, 0.827])
    
    aux_ax = 1  # Identify the number of axes in the plot.
    
    # Call extract of function. 
    # This extract is used to create the graphic and doesn't repeat the same again.
    exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A05_CallGraphic.py', encoding='utf8').read())
    code_params_output.value = ""


# %%%% [03-04-03] SHOW_CYCLIC_GRAPHIC
# This function is called when the button "show_cyclic_graphic_button" is clicked.
# Only graph the stress-strain curve of the selected files already saved as responses.

# Function to graphic stress-strain curve of selected files
def show_cyclic_graphic(change=None):
    global files_checkboxes, directory
    graph_output.value = ""
    with out:
        out.clear_output()
    
    # Find the selected files with the responses
    selected_files = [cb.description for cb in files_checkboxes if cb.value]
    # Reformat URL to be consistence
    selected_files = [direc.replace('\\', '/') for direc in selected_files]
    selected_files = [f"{directory}/{direc}" for direc in selected_files]
    directory = directory.replace('/', '\\')
    
    # Create figure
    fig = plt.figure(figsize=(11, 3.2), dpi=100)
    ax1 = fig.add_axes([0.0725, 0.133, 0.4025, 0.827])
    ax2 = fig.add_axes([0.5765, 0.133, 0.4025, 0.827])
    ax = (ax1, ax2)
    
    aux_ax = 2  # Identify the number of axes in the plot.
    
    # Call extract of function
    # This extract is used to create the graphic and doesn't repeat the same again.
    exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A05_CallGraphic.py', encoding='utf8').read())
    code_params_output.value = ""

    
# %%%% [03-04-04] SHOW_CYCLIC_VIDEO
# This function is called when the button "show_cyclic_video_button" is clicked.
# Only graph the stress-strain curve of the selected file already saved as a response.

# Function to delete and create directory for the video
def delete_and_create_directory_for_video(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    
        
# Function to graphic stress-strain curve of selected files
def show_cyclic_video(change=None):
    global files_checkboxes, directory
    global all_buttons_and_widgets_list, buttons_initial_state
    
    # Delete and create directory for the video
    delete_and_create_directory_for_video('C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/Fotogramas_Video')
    
    graph_output.value = ""
    with out:
        out.clear_output()
    
    # Disable the buttons while the video is making
    for widget in all_buttons_and_widgets_list:
        widget.disabled = True
    instructions_button.disabled = True
    
    # Obtain the selected files
    selected_files = [cb.description for cb in files_checkboxes if cb.value]
    if len(selected_files) > 1:
        graph_output.value = "Select only one file to display the video."
        code_params_output.value = ""
        
        # Enable initial widgets
        for widget in all_buttons_and_widgets_list:
            if widget in buttons_initial_state:
                widget.disabled = False
            else:
                widget.disabled = True
        
        raise Exception("Select only one file to display the video.")
    
    # Reformat URL to be consistence
    selected_files = [direc.replace('\\', '/') for direc in selected_files]
    selected_files = [f"{directory}/{direc}" for direc in selected_files]
    directory = directory.replace('/', '\\')
    
    # Create figure
    fig = plt.figure(figsize=(11, 3.2), dpi=100)
    ax1 = fig.add_axes([0.0725, 0.133, 0.4025, 0.827])
    ax2 = fig.add_axes([0.5765, 0.133, 0.4025, 0.827])
    ax = (ax1, ax2)
    
    aux_ax = 3  # Options 3 means that I'm going to make a video.
    
    # Call extract of function
    # This extract is used to create the graphic and doesn't repeat the same again.
    exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A05_CallGraphic.py', encoding='utf8').read())
    code_params_output.value = ""
    
    # Enable initial widgets
    for widget in all_buttons_and_widgets_list:
        if widget in buttons_initial_state:
            widget.disabled = False
        else:
            widget.disabled = True
    instructions_button.disabled = False


# %%%% [03-04-05] SHOW_CODE
# Function to display code of selected files
def code_selected_files(files):
    selected_files = [cb.description for cb in files if cb.value]
    # Action that you want with the checkbutton
    code_params_output.value = ""
    for url in selected_files:
        url_x = directory + "\\" + f"{url}"
        # Read the .txt files
        data_dict = TxT.read_file_to_dict(url_x)
        # Get the value of the key 'code'.
        code_value = data_dict['code']
        # Add the code to the output
        code_params_output.value = code_params_output.value + code_value + '\n\n'


def show_code(change=None):
    code_selected_files(files_checkboxes)


# %%%% [03-04-06] REFRESH_FILES
# Function to refresh the file checkboxes    
def refresh_files(change=None):
    global files_checkboxes, files_checkboxes_box, files_checkboxes_2, files_checkboxes_box_2, files_checkboxes_3, files_checkboxes_box_3
    # Refresh Checkbox of the files in the directory (re-write variable)
    files_checkboxes = list_files_with_checkboxes(directory)
    files_checkboxes_2 = list_files_with_checkboxes(directory_2)
    files_checkboxes_3 = list_files_with_checkboxes(directory_3)
    # Refresh the checkboxes in GUI
    files_checkboxes_box.children = files_checkboxes
    files_checkboxes_box_2.children = files_checkboxes_2
    files_checkboxes_box_3.children = files_checkboxes_3
    code_params_output.value = "Files have been successfully refreshed"
    graph_output.value = ""
    with out:
        out.clear_output(wait=False)


# %%%% [03-04-07] DELETE_FILE
# Function delete selected files.
def delete_file_fun(file_url: str) -> Optional[str]:
    try:
        # Parse the URL to extract the file path
        file_path = urllib.parse.urlparse(file_url).path
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            code_params_output.value = code_params_output.value + f"File '{file_path}' has been deleted successfully."
        else:
            code_params_output.value = code_params_output.value + f"File '{file_path}' does not exist."
    except Exception as e:
        code_params_output.value = code_params_output.value + f"An error occurred: {e}"


def delete_selected_files(directory_x, files) -> None:
    selected_files = [cb.description for cb in files if cb.value]
    
    if len(selected_files) != 0:
        for index, url in enumerate(selected_files):
            if index != 0:
                code_params_output.value = code_params_output.value + '\n'
            # Read the .txt files
            url_x = directory_x + "/" + f"{url}"
            delete_file_fun(url_x)


# Function to run with button.
def delete_file(change=None):
    global files_checkboxes, files_checkboxes_2, files_checkboxes_3
    code_params_output.value = ''
    
    delete_selected_files(directory, files_checkboxes)
    delete_selected_files(directory_2, files_checkboxes_2)
    delete_selected_files(directory_3, files_checkboxes_3)

    message = code_params_output.value
    refresh_files()
    code_params_output.value = message
    graph_output.value = ''
    with out:
        out.clear_output(wait=False)


# %%%% [03-04-08] DELETE_ALL
# Function to delete all files and image in the directory created for GUI
def delete_all(change=None):
    # Delete all and create new directories for .txt files.
    def recreate_directory(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    # Create all directories
    for dir_j in directories:
        recreate_directory(dir_j)

    # Annotation, refresh & clear
    refresh_files()
    code_params_output.value = 'All files have been successfully deleted.'
    graph_output.value = ''
    with out:
        out.clear_output(wait=False)


# %%%% [03-04-09] DEFINE_CYCLIC_LOAD
# Function create a .txt file with the info of the cyclic load
def define_cyclic_load(change=None):
    global all_buttons_and_widgets_list, buttons_initial_state
    global files_checkboxes_2
    widgets_to_disabled_and_enable = [id_cyclic_load_input, load_type_dropdown, cyclic_type_dropdown, 
                                      show_cyclic_load_button, define_cyclic_load_button, modify_cyclic_load_button]
    
    if define_cyclic_load_button.description == 'Define':
        define_cyclic_load_button.description = 'Save'
        define_cyclic_load_button.style.button_color = 'green'
        modify_cyclic_load_button.description = 'Cancel'
        modify_cyclic_load_button.style.button_color = 'red'
        show_cyclic_load_button.description = 'Show'
        show_cyclic_load_button.style.button_color = 'blue'
        
        # Enable key widgets
        for widget in all_buttons_and_widgets_list:
            if widget in widgets_to_disabled_and_enable:
                widget.disabled = False
            else:
                widget.disabled = True
        
        # Widgets to Define Strain Loading
        update_defo_widgets()

        # Message to user
        code_params_output.value = """Definir Strain Load:
    1. Presionar el boton Define para comenzar a definir una carga.
    2. Seleccionar una ID Load. Cuidar que este valor sea unico para cada secuencia.
    3. Seleccionar un tipo de carga: Monotonic, Cyclic.
    4. Si la solicitacion es del tipo Cyclic, seleccionar el tipo de ciclo.
    5. Presionar el boton show para visualizar la carga en el grafico.
    6. Modifica los parametros de la carga 
    Nota 1: Puede visualizar las modificaciones en la grafica en tiempo real.
    7. Presionar el boton Save para guardar la carga.
    Nota 2: En el area Strain Loadings puede visualizar el archivo creado.
Modificar Strain Load:
    1. En el area Strain Loadings, seleccione un archivo de texto.
    2. Presione el boton Edit para modificar la carga.
    3. Modifica los parametros de la carga.
    4. Presione el boton Save para guardar la carga.
"""
        # Show Graphic
        show_cyclic_load()
    
    else:
        # Create file .txt with the info of the cyclic load
        
        # Verify that the ID is unique
        actual_files = [cb.description for cb in files_checkboxes_2]
        # Example value of actual_files = ['ID_StrainLoad_1_monotonic_-.txt', 'ID_StrainLoad_2_cyclic_compression.txt']
        # Obtain the ID Mat Tag of the cyclic load.
        actual_files = [file.split('_')[2] for file in actual_files]
        # Example value of actual_files = ['1', '2']
        if str(id_cyclic_load_input.value) in actual_files:
            code_params_output.value = 'The ID Load must be unique.'
            return
        
        # Verify that the ID is positive
        if id_cyclic_load_input.value <= 0:
            code_params_output.value = 'The ID Load must be positive.'
            return 
        
        define_cyclic_load_button.description = 'Define'
        modify_cyclic_load_button.description = 'Edit'
        modify_cyclic_load_button.style.button_color = None
        define_cyclic_load_button.style.button_color = None
        show_cyclic_load_button.description = '-'
        show_cyclic_load_button.style.button_color = None
        
        # Create file .txt with the info of the cyclic load
        load_args = load_arg()
        url_strain = r'C_GUI02_uniaxialMaterial/C_GUI02_StrainLoad/ID_StrainLoad_' + str(id_cyclic_load_input.value) + f'_{load_args[0]}_{load_args[1]}.txt'
        with open(url_strain, 'w') as file:
            for item in load_args:
                file.write(f"{item}\n")
        
        # Enable initial widgets
        for widget in all_buttons_and_widgets_list:
            if widget in buttons_initial_state:
                widget.disabled = False
            else:
                widget.disabled = True
        
        # Clean the area for parameters widgets
        model_widgets.children = []
        
        # Refresh Checkbox
        refresh_files()
        
        # Message to user
        url_strain_short = '"ID_StrainLoad_' + str(id_cyclic_load_input.value) + f'_{load_args[0]}_{load_args[1]}.txt"'
        code_params_output.value = f"File {url_strain_short} has been created successfully."
    

# %%%% [03-04-10] SHOW_CYCLIC_LOAD
# Function to create graphic of strain and .txt file with info of the cyclic load.
def load_arg():
    load_type = load_type_dropdown.value
    cyclic_type = cyclic_type_dropdown.value
    load_args = []

    if load_type == 'monotonic':
        load_args = [load_type, '-', delta_e.value, e_max_c.value, e_max_t.value]
    elif load_type == 'cyclic':
        if cyclic_type == 'compression':
            load_args = [load_type, cyclic_type, delta_e.value, e_max_c_1.value, pulso_1.value, 
                         e_max_c_2.value, pulso_2.value, e_max_c_3.value, pulso_3.value, 
                         e_max_c_4.value, pulso_4.value, e_max_c_5.value, pulso_5.value]
        elif cyclic_type == 'traction':
            load_args = [load_type, cyclic_type, delta_e.value, e_max_t_1.value, pulso_1.value, 
                         e_max_t_2.value, pulso_2.value, e_max_t_3.value, pulso_3.value, 
                         e_max_t_4.value, pulso_4.value, e_max_t_5.value, pulso_5.value]
        elif cyclic_type == 'combined':
            load_args = [load_type, cyclic_type, delta_e.value, e_max_c_1.value, e_max_t_1.value, 
                         pulso_1.value, e_max_c_2.value, e_max_t_2.value, pulso_2.value, 
                         e_max_c_3.value, e_max_t_3.value, pulso_3.value, e_max_c_4.value, 
                         e_max_t_4.value, pulso_4.value, e_max_c_5.value, e_max_t_5.value, 
                         pulso_5.value]
    return load_args


# Function to show the cyclic load
def show_cyclic_load(change=None):
    load_args = load_arg()
    
    # Create figure
    fig = plt.figure(figsize=(8.5, 3.3), dpi=100)
    ax = fig.add_axes([0.105, 0.133, 0.875, 0.827])  # 0.05
    grid = True
    
    # Create strain vector and graphic
    if load_args[0] == 'monotonic':
        strains_C, strains_T = TxT.strain_load(load_args)
        Grf.plot_index_strain_only(strains_C, 'r', 'Compression', grid, ax)
        Grf.plot_index_strain_only(strains_T, 'b', 'Tension', grid, ax)
        
    elif load_args[0] == 'cyclic':
        if load_args[1] == 'compression':
            strains_C = TxT.strain_load(load_args)
            Grf.plot_index_strain_only(strains_C, 'green', 'Cyclic Compresion', grid, ax)
        elif load_args[1] == 'traction':
            strains_T = TxT.strain_load(load_args)
            Grf.plot_index_strain_only(strains_T, 'brown', 'Cyclic Tension', grid, ax)
        elif load_args[1] == 'combined':
            strains_D = TxT.strain_load(load_args)
            Grf.plot_index_strain_only(strains_D, 'magenta', 'Cyclic Combined', grid, ax)
    
    # Save figure
    url = r'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/strain_load'
    url = url + '_' + load_args[0] + '_' + load_args[1] + '.png'
    
    # Annotation
    graph_output.value = str(url)
    ax.invert_yaxis()
    
    # Save
    plt.savefig(url)
    plt.close()
    
    # Display the image
    with out:
        out.clear_output()
        display(Image(filename=url))


# %%%% [03-04-11] MODIFY_STRAIN_FILE
# Function to read the selected .txt files
def read_selected_files_strain(files, aux_checkbox = True):
    global code_params_output
    
    if aux_checkbox:
        # Select only the files that are checked.
        selected_files = [cb.description for cb in files if cb.value]
        
        # Verify that the selected files are only one
        if len(selected_files) > 1:
            code_params_output.value = "Select only one file to modify the strain."
            return []
        elif len(selected_files) == 0:
            code_params_output.value = "Select a file to modify the strain."
            return []
        
        # URL to read the .txt files
        url_x = directory_2 + "/" + f"{selected_files[0]}"
        # Obtain the ID of the cyclic load
        filename = selected_files[0]
        # Split the string by '_'
        parts = filename.split('_')
        # The number is the third element in the list (index 2)
        ID_cyclic_strain = parts[2]
        
    else:
        selected_files = files
        url_x = f"{selected_files[0]}"
        ID_cyclic_strain = 'Default'

    # Read the .txt files and create a list with the data of the file
    with open(url_x, 'r') as file:
        load_args = [line.strip() for line in file.readlines()]
        
    return load_args, ID_cyclic_strain


# Function to assign the values of the file to the widgets
def assign_values_to_load_args(load_args: list) -> None:
    global load_type_dropdown, cyclic_type_dropdown, delta_e, e_max_c, e_max_t, e_max_c_1, e_max_c_2, e_max_c_3, e_max_c_4, e_max_c_5
    global e_max_t_1, e_max_t_2, e_max_t_3, e_max_t_4, e_max_t_5, pulso_1, pulso_2, pulso_3, pulso_4, pulso_5
    
    load_type = load_args[0]
    load_type_dropdown.value = load_type
    cyclic_type = load_args[1]
    cyclic_type_dropdown.value = cyclic_type
    if load_type == 'monotonic':
        delta_e.value = load_args[2]
        e_max_c.value = load_args[3]
        e_max_t.value = load_args[4]
    elif load_type == 'cyclic':
        if cyclic_type == 'compression':
            delta_e.value = load_args[2]
            e_max_c_1.value = load_args[3]
            pulso_1.value = load_args[4]
            e_max_c_2.value = load_args[5]
            pulso_2.value = load_args[6]
            e_max_c_3.value = load_args[7]
            pulso_3.value = load_args[8]
            e_max_c_4.value = load_args[9]
            pulso_4.value = load_args[10]
            e_max_c_5.value = load_args[11]
            pulso_5.value = load_args[12]
        elif cyclic_type == 'traction':
            delta_e.value = load_args[2]
            e_max_t_1.value = load_args[3]
            pulso_1.value = load_args[4]
            e_max_t_2.value = load_args[5]
            pulso_2.value = load_args[6]
            e_max_t_3.value = load_args[7]
            pulso_3.value = load_args[8]
            e_max_t_4.value = load_args[9]
            pulso_4.value = load_args[10]
            e_max_t_5.value = load_args[11]
            pulso_5.value = load_args[12]
        elif cyclic_type == 'combined':
            delta_e.value = load_args[2]
            e_max_c_1.value = load_args[3]
            e_max_t_1.value = load_args[4]
            pulso_1.value = load_args[5]
            e_max_c_2.value = load_args[6]
            e_max_t_2.value = load_args[7]
            pulso_2.value = load_args[8]
            e_max_c_3.value = load_args[9]
            e_max_t_3.value = load_args[10]
            pulso_3.value = load_args[11]
            e_max_c_4.value = load_args[12]
            e_max_t_4.value = load_args[13]
            pulso_4.value = load_args[14]
            e_max_c_5.value = load_args[15]
            e_max_t_5.value = load_args[16]
            pulso_5.value = load_args[17]
    
    
# Function to modify strain of cyclic load
def modify_cyclic_load(change=None):
    global observer_enabled  # Variable to enable or disable the observer
    global files_checkboxes_2, id_cyclic_load_input
    global files_checkboxes, files_checkboxes_3
    
    # Verify that only have one file selected
    selected_files_1 = [cb.description for cb in files_checkboxes if cb.value]
    selected_files_2 = [cb.description for cb in files_checkboxes_2 if cb.value]
    selected_files_3 = [cb.description for cb in files_checkboxes_3 if cb.value]
    total_selected_files = len(selected_files_1) + len(selected_files_2) + len(selected_files_3)
    if total_selected_files > 1:
        code_params_output.value = "Select only one file to modify the material model."
        return
    
    # If modify_cyclic_load_button is 'Edit', the code will modify the strain of the selected file
    if modify_cyclic_load_button.description == 'Edit':
        # Don't update the observer
        observer_enabled = False
        
        # Read the selected .txt files
        load_args, ID_cyclic_strain = read_selected_files_strain(files_checkboxes_2)
        
        if len(load_args) != 0:
            # Activate the widgets and format to modify cyclic strain load
            define_cyclic_load()
            
            # In this special case, when I edit a file with load strain If I cancel it, it will be deleted.
            modify_cyclic_load_button.description = 'Delete'
            
            # Assign the values of the file to the widgets
            assign_values_to_load_args(load_args)
            id_cyclic_load_input.value = int(ID_cyclic_strain)

            # Display graphic
            show_cyclic_load()
            
            # Message to user
            code_params_output.value = """Definir Strain Load:
    1. Presionar el boton Define para comenzar a definir una carga.
    2. Seleccionar una ID Load. Cuidar que este valor sea unico para cada secuencia.
    3. Seleccionar un tipo de carga: Monotonic, Cyclic.
    4. Si la solicitacion es del tipo Cyclic, seleccionar el tipo de ciclo.
    5. Presionar el boton show para visualizar la carga en el grafico.
    6. Modifica los parametros de la carga 
    Nota 1: Puede visualizar las modificaciones en la grafica en tiempo real.
    7. Presionar el boton Save para guardar la carga.
    Nota 2: En el area Strain Loadings puede visualizar el archivo creado.
Modificar Strain Load:
    1. En el area Strain Loadings, seleccione un archivo de texto.
    2. Presione el boton Edit para modificar la carga.
    3. Modifica los parametros de la carga.
    4. Presione el boton Save para guardar la carga.
    """
            # After load the file, the code will delete the file.
            delete_file()
            
            # Refresh the graphic
            show_cyclic_load()
            
            # Enable the observer
            observer_enabled = True


    # If modify_cyclic_load_button is 'Cancel', the code will cancel the definition of the cyclic load
    elif modify_cyclic_load_button.description == 'Cancel' or modify_cyclic_load_button.description == 'Delete':
        define_cyclic_load_button.description = 'Define'
        modify_cyclic_load_button.description = 'Edit'
        modify_cyclic_load_button.style.button_color = None
        define_cyclic_load_button.style.button_color = None
        add_file_button.style.button_color = None
        show_cyclic_load_button.description = '-'
        show_cyclic_load_button.style.button_color = None
        
        # Enable initial widgets
        for widget in all_buttons_and_widgets_list:
            if widget in buttons_initial_state:
                widget.disabled = False
            else:
                widget.disabled = True
        
        # Clean the area for parameters widgets
        model_widgets.children = []
        
        # Refresh Checkbox
        refresh_files()
        
        # Message to user
        code_params_output.value = 'The definition of the cyclic load has been canceled.'


# %%%% [03-04-12] DEFINE_MATERIAL_MODEL
# Function to create a .txt file with the info of the material model
# Note that this function is similar to define_cyclic_load
def define_material_model(change=None):
    global all_buttons_and_widgets_list, buttons_initial_state
    global files_checkboxes_3
    widgets_to_disabled_and_enable = [show_material_model_button, MatTag_input, material_type_dropdown,
                                       model_type_dropdown, unit_dropdown, graphic_unit_dropdown,
                                       strain_loading_dropdown, define_material_model_button,
                                       add_file_button, see_instruction_button, modify_material_model_button]
    
    if define_material_model_button.description == 'Define':
        define_material_model_button.description = 'Save'
        define_material_model_button.style.button_color = 'green'
        modify_material_model_button.description = 'Cancel'
        modify_material_model_button.style.button_color = 'red'
        show_material_model_button.description = 'Show'
        show_material_model_button.style.button_color = 'blue'
        add_file_button.style.button_color = 'brown'
        
        # Enable key widgets
        for widget in all_buttons_and_widgets_list:
            if widget in widgets_to_disabled_and_enable:  # and widget != modify_cyclic_load_button
                widget.disabled = False
            else:
                widget.disabled = True
        
        if material_type_dropdown.value != 'MinMax':
            # Refresh Dropdown
            update_model_type_dropdown()
            # Widgets to Define Model
            update_model_widgets()
            # Show Graphic
            show_material_model()
        else:      
            # material_type_dropdown.options = ['Concrete', 'Steel', 'MinMax', 'User defined']
            material_type_dropdown.value = 'Concrete'  # Initial value to avoid errors
            # Refresh Dropdown
            update_model_type_dropdown()
            # Widgets to Define Model
            update_model_widgets()
        
        # Message to user
        code_params_output.value = """Definir Material Model:
    1. Presionar el boton Define Material Model para comenzar a definir el modelo.
    2. Seleccionar un Material Tag unico para cada modelo definido.
    3. Seleccionar el tipo de material.
    4. Seleccionar el modelo a emplear.
    5. Seleccionar las unidades a emplear en el modelo.
    7. Seleccionar un archivo de texto Strain Load para visualizar el comportamiento del material.
    8. Seleccione las unidades de la grafica.
    9. Presione el boton show para visualizar el comportamiento del material.
    10. Modificar los parametros del material.
    Nota 1: Puede visualizar las modificaciones en la grafica en tiempo real.
    11. Presionar el boton Save para guardar el modelo.
    Nota 2: En el area Material Model puede visualizar el archivo creado.
Modificar Material Model:
    1. En el area Material Model, seleccione un archivo de texto.
    2. Presione el boton Edit para modificar el modelo.
    3. Modifica los parametros del material.
    4. Presione el boton Save para guardar el modelo."""

    
    else:
        # Verify that the ID is unique
        actual_files = [cb.description for cb in files_checkboxes_3]
        # Example value of actual_files = ['MatTag_1_Saatcioglu(1992).txt', 'MatTag_2_ConcreteCM.txt']
        # Obtain the MatTag of the material model.
        actual_files = [file.split('_')[1] for file in actual_files]
        # Example value of actual_files = ['1', '2']
        if str(MatTag_input.value) in actual_files:
            code_params_output.value = 'The Mat Tag must be unique.'
            return
        
        # Verify that the ID is positive
        if MatTag_input.value <= 0:
            code_params_output.value = 'The Mat Tag must be positive.'
            return
        
        define_material_model_button.description = 'Define'
        modify_material_model_button.description = 'Edit'
        modify_material_model_button.style.button_color = None
        define_material_model_button.style.button_color = None
        show_material_model_button.description = '-'
        show_material_model_button.style.button_color = None
        show_material_model_button.disabled = True
        add_file_button.style.button_color = None
        
        # Create file .txt with the info of the material model
        # There are two possible situations:
        # 1. The user define a Concrete/Steel/User defined material model. It implies use model_arg() function.
        # 2. The user define a MinMax material model. It implies use min_max_model_arg() function.
        if material_type_dropdown.value == 'MinMax':
            model_args = min_max_model_arg()
        else:
            model_args = model_arg()
        
        unit = unit_dropdown.value
        material_type = material_type_dropdown.value
        
        url_material = r'C_GUI02_uniaxialMaterial/C_GUI02_MaterialModel/MatTag_' + str(MatTag_input.value) + f'_{model_args[0]}.txt'
        with open(url_material, 'w') as file:
            file.write(f"{material_type}\n")
            file.write(f"{unit}\n")
            for item in model_args:
                file.write(f"{item}\n")
        
        # Enable initial widgets
        for widget in all_buttons_and_widgets_list:
            if widget in buttons_initial_state:
                widget.disabled = False
            else:
                widget.disabled = True
        
        # Clean the area for parameters widgets
        model_widgets.children = []
        
        # Refresh Checkbox
        refresh_files()
        
        # Message to user
        url_material_short = '"MatTag_' + str(MatTag_input.value) + f'_{model_args[0]}.txt"'
        code_params_output.value = f"File {url_material_short} has been created successfully."

        # Hide the regularizations widgets
        regularization_widgets.children = []
        

# %%%% [03-04-13] SHOW_MATERIAL_MODEL_REAL_TIME
# Function to capture the arguments of the material model.
# This function is used to graph the material model in real time, and for create the .txt file.
def model_arg():
    model_type = model_type_dropdown.value
    model_args = []

    if model_type == 'ConcreteCM':
        model_args = [model_type_dropdown.value, MatTag_input.value, fpcc_input.value, epcc_input.value,
                        Ec_input.value, rc_input.value, xcrn_input.value, ft_input.value, et_input.value,
                        rt_input.value, xcrp_input.value, GapClose_input.value]
    elif model_type == 'Concrete07':
        model_args = [model_type_dropdown.value, MatTag_input.value, fc_input.value, epsc_input.value,
                        Ec_input.value, ft_input.value, et_input.value, xp_input.value, xn_input.value, r_input.value]

    elif model_type == 'SteelMPF':
        model_args = [model_type_dropdown.value, MatTag_input.value, fyp_input.value, fyn_input.value,
                        E0_input.value, bp_input.value, bn_input.value, R0_input.value, cR1_input.value,
                        cR2_input.value, a1_input.value, a2_input.value, a3_input.value, a4_input.value]
    
    elif model_type == 'Steel02':
        model_args = [model_type_dropdown.value, MatTag_input.value, Fy_Steel02_input.value, E0_Steel02_input.value,
                      b_Steel02_input.value, R0_Steel02_input.value, cR1_Steel02_input.value, cR2_Steel02_input.value,
                      a1_Steel02_input.value, a2_Steel02_input.value, a3_Steel02_input.value, a4_Steel02_input.value,
                      sigInit_Steel02_input.value]
    
    elif model_type == 'Steel01':
        model_args = [model_type_dropdown.value, MatTag_input.value, Fy_Steel01_input.value, E0_Steel01_input.value,
                      b_Steel01_input.value, a1_Steel01_input.value, a2_Steel01_input.value, a3_Steel01_input.value,
                        a4_Steel01_input.value]
    
    elif model_type == 'Steel4':
        model_args = [model_type_dropdown.value, MatTag_input.value, Fy_Steel4_input.value, E0_Steel4_input.value,
                      b_k_Steel4_input.value, R0_Steel4_input.value, r1_Steel4_input.value, r2_Steel4_input.value,
                      b_kc_Steel4_input.value, R0c_Steel4_input.value, r1c_Steel4_input.value, r2c_Steel4_input.value,
                      b_i_Steel4_input.value, rho_i_Steel4_input.value, b_I_Steel4_input.value, R_i_Steel4_input.value,
                      I_yp_Steel4_input.value, b_ic_Steel4_input.value, rho_ic_Steel4_input.value, b_Ic_Steel4_input.value,
                      R_ic_Steel4_input.value, f_u_Steel4_input.value, R_u_Steel4_input.value, f_uc_Steel4_input.value, 
                      R_uc_Steel4_input.value, sig_init_Steel4_input.value, cycNum_Steel4_input.value]

    elif model_type == 'Saatcioglu(1992)':
        model_args = [model_type_dropdown.value, MatTag_input.value, fco_input.value, fl_input.value,
                        e01_input.value,
                        rho_input.value, e085_input.value]
        
    elif model_type == 'Mander(1988)':
        model_args = [model_type_dropdown.value, MatTag_input.value, fco_input.value, CSR_input.value,
                        eco_input.value,
                        Ec_input.value]
        
    elif model_type == 'Belarbi(1994)':
        model_args = [model_type_dropdown.value, MatTag_input.value, f_cr_input.value, 
                      eps_cr_input.value, Ecr_input.value]
        
    return model_args


# Function to save .txt file of the MinMax material and for graph the material model in real time
def min_max_model_arg():
    material_type = material_type_dropdown.value
    min_max_model_args = []
    
    if material_type == 'MinMax':
        min_max_model_args = [material_type, MatTag_minmax_input.value, OtherTag_minmax_dropdown.value, 
                              minStrain_input.value, maxStrain_input.value]
    return min_max_model_args


# Function to create argument for function (.txt)
def url_arg(load_type, cyclic_type):
    url1 = ''
    if load_type == 'monotonic':
        url1 = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/monotonic/'
    elif load_type == 'cyclic':
        if cyclic_type == 'compression':
            url1 = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/cyclic_compression/'
        elif cyclic_type == 'traction':
            url1 = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/cyclic_traction/'
        elif cyclic_type == 'combined':
            url1 = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/cyclic_combined/'
    return url1


# Function to create the file with the model and the result of test it. 
def create_material_model_test_file(selected_file_in_strain_dropdown, aux_checkbox = True):
    
    # Define the cyclic load arguments. If aux_checkbox = False, use default value
    if aux_checkbox:
        load_args, ID_cyclic_strain = read_selected_files_strain(selected_file_in_strain_dropdown)
    else:
        load_args, ID_cyclic_strain = read_selected_files_strain(selected_file_in_strain_dropdown, aux_checkbox = False)
    
    # Define the unit of the model
    unit = unit_dropdown.value

    # Define the material model arguments
    # There are two possible situations:
    # 1. The user define a MinMax material model.
    #    - This implies pass to the TxT.data_plot aditional arguments. 
    #    - The model_args of the original material, and the model args of the MinMax material.
    # 2. The user define a Concrete/Steel/User defined material model.
    #    - It implies only pass the default argument to the TxT.data_plot function.
    if material_type_dropdown.value == 'MinMax':
        model_args = model_arg()
        min_max_args = min_max_model_arg()
        
        # I'm not going to create a .txt file with the response of the material for the load that 
        # is on going definition, I'm going only to create de dictionary with that data. 
        # Because I don't want to write a txt file an read it.
        dictionary = TxT.data_plot(unit, model_args, load_args, min_max_args_x = min_max_args)  # dictionary['DataPlot']
        
    else:
        model_args = model_arg()

        # I'm not going to create a .txt file with the response of the material for the load that 
        # is on going definition, I'm going only to create de dictionary with that data. 
        # Because I don't want to write a txt file an read it.
        dictionary = TxT.data_plot(unit, model_args, load_args)  # dictionary['DataPlot']
        
    return dictionary
    

# Function to create graphic of stress-strain curve of material model
def show_material_model(change=None):
    global files_checkboxes_2, files_checkboxes, directory, selected_strain_dropdown
    with out:
        out.clear_output()
    graph_output.value = ""
    code_params_output.value = ""
    
    # Obtain the selected value of the strain loading dropdown
    selected_strain_dropdown = strain_loading_dropdown.value

    # If there aren't selected files, give a message to the user and use default values
    if selected_strain_dropdown == '-':
        
        # Graph another model to compare behavior  (.txt files from Responses checkbox)
        selected_files = [cb.description for cb in files_checkboxes if cb.value]
        # Reformat URL to be consistence
        selected_files = [direc.replace('\\', '/') for direc in selected_files]
        selected_files = [f"{directory}/{direc}" for direc in selected_files]
        directory = directory.replace('/', '\\')
        
        code_params_output.value = """Select a 'Strain load' to create the material model and see in real time the behavior of the material.
If there are not files selected, it will use default values as 'Strain load'."""

        # Create the graphic with the default values
        selected_files_default = ['C_GUI02_uniaxialMaterial/ID_StrainLoad_99_monotonic_-.txt']
        
        # Create dictionary with the data of the material model and the strain load
        # The model is defined in base of the parameters in the GUI
        dictionary = create_material_model_test_file(selected_files_default, aux_checkbox = False)
        
        # Data to graphic
        url_file = 'Dictionary_with_direct_data'
        
        # Create figure
        fig = plt.figure(figsize=(6.875, 4), dpi=100)
        ax = fig.add_axes([0.145, 0.133, 0.805, 0.827])
        aux_ax = 1  # Identify the number of axes in the plot.
        
        # Graph the file created with the material model tested    
        selected_files.insert(0, url_file)
        
        # Plot the regularization if it is activated
        if regularization_button.description == 'Hide':            
            nodes = calculate_nodes_area_regularization_post_peak()
            
            # Create a polygon patch with the given nodes
            quad = patches.Polygon(nodes, closed=True, color='skyblue', alpha=0.8)
            # Add the polygon patch to the axis
            ax.add_patch(quad)
        
        # Call extract of function to graphic the stress-strain curve.
        exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A05_CallGraphic.py', encoding='utf8').read())
        
    else:
        code_params_output.value = ''
        
        # Graph another model to compare behavior  (.txt files from Responses checkbox)
        selected_files = [cb.description for cb in files_checkboxes if cb.value]
        # Reformat URL to be consistence
        selected_files = [direc.replace('\\', '/') for direc in selected_files]
        selected_files = [f"{directory}/{direc}" for direc in selected_files]
        directory = directory.replace('/', '\\')

        # Create a list with a unique value. This value is the file with the strain loading selected 
        # This is necessary to reutilize the function read_selected_files_strain
        selected_file_in_strain_dropdown = [cb for cb in files_checkboxes_2 if cb.description == selected_strain_dropdown]
        
        # Activate the checkbox of the selected value in the list, to use the function read_selected_files_strain
        selected_file_in_strain_dropdown[0].value = True
        
        # The model is defined in base of the parameters in the GUI
        dictionary = create_material_model_test_file(selected_file_in_strain_dropdown, aux_checkbox = True)
        
        # Disable the checkbox of the selected value in the list, to use the function read_selected_files_strain
        selected_file_in_strain_dropdown[0].value = False
        
        # Data to graphic
        url_file = 'Dictionary_with_direct_data'

        # Create figure
        fig = plt.figure(figsize=(6.875, 4), dpi=100)
        ax = fig.add_axes([0.145, 0.133, 0.805, 0.827])
        aux_ax = 1  # Identify the number of axes in the plot.
        
        # Graph the file created with the material model tested    
        selected_files.insert(0, url_file)
        
        # Plot the regularization if it is activated
        if regularization_button.description == 'Hide':            
            nodes = calculate_nodes_area_regularization_post_peak()
            
            # Create a polygon patch with the given nodes
            quad = patches.Polygon(nodes, closed=True, color='skyblue', alpha=0.8)
            # Add the polygon patch to the axis
            ax.add_patch(quad)

        # Call extract of function to graphic the stress-strain curve.
        exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A05_CallGraphic.py', encoding='utf8').read())


# %%%% [03-04-14] MODIFY_MATERIAL_MODEL
# Function to read_selected_files_model
def read_selected_files_model(selected_file):
    global code_params_output
    
    # Read the .txt files
    url_x = directory_3 + "/" + f"{selected_file}"
    
    # Read the .txt files and create a list with the data of the file
    with open(url_x, 'r') as file:
        model_args_prev = [line.strip() for line in file.readlines()]
    
    # Obtain the material type of the model: Concrete, Steel, User defined, MinMax
    material_type = model_args_prev[0]
    # Obtain the units of the model
    unit_model = model_args_prev[1]
    # Assign the rest of the values to the variable model_args
    model_args = model_args_prev[2:]
    return model_args, unit_model, material_type


# Function to assign the values of the file to the widgets
def assign_values_to_model_args(model_args, unit_model, material_type) -> None:
    global unit_dropdown, material_type_dropdown, model_type_dropdown, MatTag_input
    global fpcc_input, epcc_input, Ec_input, rc_input, xcrn_input, ft_input, et_input, rt_input, xcrp_input, GapClose_input
    global fc_input, epsc_input, xp_input, xn_input, r_input
    global fyp_input, fyn_input, E0_input, bp_input, bn_input, R0_input, cR1_input, cR2_input, a1_input, a2_input, a3_input, a4_input
    global fco_input, fl_input, e01_input, rho_input, e085_input, CSR_input
    global eco_input
    global OtherTag_minmax_dropdown, minStrain_input, maxStrain_input, MatTag_minmax_input
    global observer_enabled
    global Fy_Steel02_input, E0_Steel02_input, b_Steel02_input, R0_Steel02_input, cR1_Steel02_input, cR2_Steel02_input
    global a1_Steel02_input, a2_Steel02_input, a3_Steel02_input, a4_Steel02_input, sigInit_Steel02_input
    global Fy_Steel01_input, E0_Steel01_input, b_Steel01_input, a1_Steel01_input, a2_Steel01_input, a3_Steel01_input, a4_Steel01_input
    global Fy_Steel4_input, E0_Steel4_input, b_k_Steel4_input, R0_Steel4_input, r1_Steel4_input, r2_Steel4_input
    global b_kc_Steel4_input, R0c_Steel4_input, r1c_Steel4_input, r2c_Steel4_input, b_i_Steel4_input, rho_i_Steel4_input
    global b_I_Steel4_input, R_i_Steel4_input, I_yp_Steel4_input, b_ic_Steel4_input, rho_ic_Steel4_input, b_Ic_Steel4_input
    global R_ic_Steel4_input, f_u_Steel4_input, R_u_Steel4_input, f_uc_Steel4_input, R_uc_Steel4_input, sig_init_Steel4_input
    global cycNum_Steel4_input
    
    # Assign the values of the file to the widgets
    unit_dropdown.value = unit_model
    
    observer_enabled = False    # I have the trouble to put an observer in the dropdowns.
                                # In this observer I change the value of observer enabled.
                                # For that I have to disable it again when I assign values
                                # to a widget from a file text. 
    material_type_dropdown.value = material_type
    
    # In the case of MinMax material, it isn't necessary to assign the values of the model that modify the MinMax model
    if model_args[0] == 'MinMax':
        minStrain_input.value = model_args[3]
        maxStrain_input.value = model_args[4]
        update_otherTag_minmax_dropdown()
        OtherTag_minmax_dropdown.value = model_args[2]
        MatTag_minmax_input.value = int(model_args[1])
        update_otherTag_parameters()

    else:
        model_type_dropdown.value = model_args[0]
        MatTag_input.value = int(model_args[1])
    
    if model_args[0] == 'ConcreteCM':
        fpcc_input.value = model_args[2]
        epcc_input.value = model_args[3]
        Ec_input.value = model_args[4]
        rc_input.value = model_args[5]
        xcrn_input.value = model_args[6]
        ft_input.value = model_args[7]
        et_input.value = model_args[8]
        rt_input.value = model_args[9]
        xcrp_input.value = model_args[10]
        GapClose_input.value = model_args[11]
    elif model_args[0] == 'Concrete07':
        fc_input.value = model_args[2]
        epsc_input.value = model_args[3]
        Ec_input.value = model_args[4]
        ft_input.value = model_args[5]
        et_input.value = model_args[6]
        xp_input.value = model_args[7]
        xn_input.value = model_args[8]
        r_input.value = model_args[9]
    elif model_args[0] == 'SteelMPF':
        fyp_input.value = model_args[2]
        fyn_input.value = model_args[3]
        E0_input.value = model_args[4]
        bp_input.value = model_args[5]
        bn_input.value = model_args[6]
        R0_input.value = model_args[7]
        cR1_input.value = model_args[8]
        cR2_input.value = model_args[9]
        a1_input.value = model_args[10]
        a2_input.value = model_args[11]
        a3_input.value = model_args[12]
        a4_input.value = model_args[13]
    elif model_args[0] == 'Steel02':
        Fy_Steel02_input.value = model_args[2]
        E0_Steel02_input.value = model_args[3]
        b_Steel02_input.value = model_args[4]
        R0_Steel02_input.value = model_args[5]
        cR1_Steel02_input.value = model_args[6]
        cR2_Steel02_input.value = model_args[7]
        a1_Steel02_input.value = model_args[8]
        a2_Steel02_input.value = model_args[9]
        a3_Steel02_input.value = model_args[10]
        a4_Steel02_input.value = model_args[11]
        sigInit_Steel02_input.value = model_args[12]
    elif model_args[0] == 'Steel01':
        Fy_Steel01_input.value = model_args[2]
        E0_Steel01_input.value = model_args[3]
        b_Steel01_input.value = model_args[4]
        a1_Steel01_input.value = model_args[5]
        a2_Steel01_input.value = model_args[6]
        a3_Steel01_input.value = model_args[7]
        a4_Steel01_input.value = model_args[8]
    elif model_args[0] == 'Steel4':
        Fy_Steel4_input.value = model_args[2]
        E0_Steel4_input.value = model_args[3]
        b_k_Steel4_input.value = model_args[4]
        R0_Steel4_input.value = model_args[5]
        r1_Steel4_input.value = model_args[6]
        r2_Steel4_input.value = model_args[7]
        b_kc_Steel4_input.value = model_args[8]
        R0c_Steel4_input.value = model_args[9]
        r1c_Steel4_input.value = model_args[10]
        r2c_Steel4_input.value = model_args[11]
        b_i_Steel4_input.value = model_args[12]
        rho_i_Steel4_input.value = model_args[13]
        b_I_Steel4_input.value = model_args[14]
        R_i_Steel4_input.value = model_args[15]
        I_yp_Steel4_input.value = model_args[16]
        b_ic_Steel4_input.value = model_args[17]
        rho_ic_Steel4_input.value = model_args[18]
        b_Ic_Steel4_input.value = model_args[19]
        R_ic_Steel4_input.value = model_args[20]
        f_u_Steel4_input.value = model_args[21]
        R_u_Steel4_input.value = model_args[22]
        f_uc_Steel4_input.value = model_args[23]
        R_uc_Steel4_input.value = model_args[24]
        sig_init_Steel4_input.value = model_args[25]
        cycNum_Steel4_input.value = model_args[26]
    elif model_args[0] == 'Saatcioglu(1992)':
        fco_input.value = model_args[2]
        fl_input.value = model_args[3]
        e01_input.value = model_args[4]
        rho_input.value = model_args[5]
        e085_input.value = model_args[6]
    elif model_args[0] == 'Mander(1988)':
        fco_input.value = model_args[2]
        CSR_input.value = model_args[3]
        eco_input.value = model_args[4]
        Ec_input.value = model_args[5]
    elif model_args[0] == 'Belarbi(1994)':
        f_cr_input.value = model_args[2]
        eps_cr_input.value = model_args[3]
        Ecr_input.value = model_args[4]


# Function to modify the material model
def modify_material_model(change=None):
    global observer_enabled  # Variable to enable or disable the observer
    global files_checkboxes_3, MatTag_input
    global files_checkboxes, files_checkboxes_2
     
    # Verify that only have one file is selected
    selected_files_1 = [cb.description for cb in files_checkboxes if cb.value]
    selected_files_2 = [cb.description for cb in files_checkboxes_2 if cb.value]
    selected_files_3 = [cb.description for cb in files_checkboxes_3 if cb.value]
    total_selected_files = len(selected_files_1) + len(selected_files_2) + len(selected_files_3)
    if total_selected_files > 1:
        code_params_output.value = "Select only one file to modify the material model."
        return
        
    # If modify_material_model_button is 'Edit', the code will modify the material model of the selected file
    if modify_material_model_button.description == 'Edit':  
        # Don't update the observer to avoid generate a new graph each time a parameter is updated
        observer_enabled = False
        
        # Verify that the selected files is a material model.
        if len(selected_files_3) == 0:
            code_params_output.value = "Select a file to modify the material model."
            return
        
        # Obtain the parameters in the model .txt file
        model_args, unit_model, material_type = read_selected_files_model(selected_files_3[0])
        
        # Update the widgets and their value with the values of the file
        if len(model_args) != 0:
            # Activate the widgets and format to modify the material model
            material_type_dropdown.value = 'Concrete'  # Impose this initial value to avoid errors
            model_type_dropdown.value = 'ConcreteCM'  # Impose this initial value to avoid errors
            define_material_model()
            
            # In this special case, when I edit a file with load strain If I cancel it, it will be deleted.
            modify_material_model_button.description = 'Delete'
            
            # Assign the values of the file to the widgets
            assign_values_to_model_args(model_args, unit_model, material_type)
                        
            # Message to user
            code_params_output.value = """Definir Strain Load:
    1. Presionar el boton Define para comenzar a definir una carga.
    2. Seleccionar una ID Load. Cuidar que este valor sea unico para cada secuencia.
    3. Seleccionar un tipo de carga: Monotonic, Cyclic.
    4. Si la solicitacion es del tipo Cyclic, seleccionar el tipo de ciclo.
    5. Presionar el boton show para visualizar la carga en el grafico.
    6. Modifica los parametros de la carga 
    Nota 1: Puede visualizar las modificaciones en la grafica en tiempo real.
    7. Presionar el boton Save para guardar la carga.
    Nota 2: En el area Strain Loadings puede visualizar el archivo creado.
Modificar Strain Load:
    1. En el area Strain Loadings, seleccione un archivo de texto.
    2. Presione el boton Edit para modificar la carga.
    3. Modifica los parametros de la carga.
    4. Presione el boton Save para guardar la carga.
    """
            # After load the file, the code will delete the file.
            delete_file()
            
            # Display graphic
            show_material_model()
            
            
    # If modify_material_model_button is 'Cancel', the code will cancel the definition of the material model
    elif modify_material_model_button.description == 'Cancel' or modify_material_model_button.description == 'Delete':
        define_material_model_button.description = 'Define'
        modify_material_model_button.description = 'Edit'
        modify_material_model_button.style.button_color = None
        define_material_model_button.style.button_color = None
        show_material_model_button.description = '-'
        show_material_model_button.style.button_color = None
        add_file_button.style.button_color = None
        
        # Enable initial widgets
        for widget in all_buttons_and_widgets_list:
            if widget in buttons_initial_state:
                widget.disabled = False
            else:
                widget.disabled = True
        
        # Clean the area for parameters widgets
        model_widgets.children = []
        
        # Refresh Checkbox
        refresh_files()
        
        # Message to user
        code_params_output.value = 'The definition of the material model has been canceled.'

        # Hide the regularizations widgets
        regularization_widgets.children = []
        
    # Enable the observer
    observer_enabled = True

# %%%% [03-04-15] REGULARIZE_MATERIAL
# Function to calculate the vertices of the polygon to regularize the material.
def calculate_nodes_area_regularization_post_peak(change=None):
    global unit_factors_new
    
    # Obtain the unit of the graphic and model
    graphic_unit = graphic_unit_dropdown.value
    model_unit = unit_dropdown.value
    
    # Obtain the values of the peak stress and strain
    fc = fc_reg_input.value
    Ec = Ec_reg_input.value
    ec = ec_reg_input.value
    
    fc = float(fc)
    Ec = float(Ec)
    ec = float(ec)
    
    fc = abs(fc)
    Ec = abs(Ec)
    ec = abs(ec)
    
    fc = fc * unit_factors_new[graphic_unit][model_unit]
    Ec = Ec * unit_factors_new[graphic_unit][model_unit]
    
    # Obtain the regularization parameters
    fr = fr_reg_input.value
    Gfc_cc = Gfc_cc_input.value
    L_reg = L_reg_input.value
    
    fr = float(fr)
    Gfc_cc = float(Gfc_cc)
    L_reg = float(L_reg)
    
    fr = abs(fr)
    Gfc_cc = abs(Gfc_cc)
    L_reg = abs(L_reg)
    
    Gf_L = Gfc_cc / L_reg
    fr = fr * unit_factors_new[graphic_unit][model_unit]
    Gf_L = Gf_L * unit_factors_new[graphic_unit][model_unit]
    
    # Calculate epsilon_y
    eps_y = ec - fc/Ec + fr/Ec
    
    # Calculate epsilon_r
    eps_r = Gf_L*2/(fr+fc)+eps_y
    
    # Calculate epsilon_delta_y
    eps_delt_y = fr/Ec
    
    # Calculate the coordinates of the polygon
    eps_1 = eps_y - eps_delt_y
    fc_r_1 = 0
    eps_2 = eps_r - eps_delt_y
    fc_r_2 = 0
    eps_3 = eps_r
    fc_r_3 = fr
    eps_4 = ec
    fc_r_4 = fc
    
    
    # Assign the correct sign to the variables
    fc_r_1 = -fc_r_1
    fc_r_2 = -fc_r_2
    fc_r_3 = -fc_r_3
    fc_r_4 = -fc_r_4
    eps_1 = -eps_1
    eps_2 = -eps_2
    eps_3 = -eps_3
    eps_4 = -eps_4
    
    nodes = [(eps_1, fc_r_1), (eps_2, fc_r_2), (eps_3, fc_r_3), (eps_4, fc_r_4)]
    
    return nodes


# Function to regularize the material
def regularize_material(change=None):
    if regularization_button.description == 'Post-peak Regularization':
        nodes = calculate_nodes_area_regularization_post_peak()
        [(eps_1, fc_r_1), (eps_2, fc_r_2), (eps_3, fc_r_3), (eps_4, fc_r_4)] = nodes
        
        regularization_button.description = 'Hide'
        
        fc_reg_input.disabled = True
        ec_reg_input.disabled = True
        Ec_reg_input.disabled = True
        fr_reg_input.disabled = True
        Gfc_cc_input.disabled = True
        L_reg_input.disabled = True
        show_material_model()
        
        code_params_output.value = code_params_output.value + f"\neps_r = {eps_3}"
    
    else:
        regularization_button.description = 'Post-peak Regularization'
        
        fc_reg_input.disabled = False
        ec_reg_input.disabled = False
        Ec_reg_input.disabled = False
        fr_reg_input.disabled = False
        Gfc_cc_input.disabled = False
        L_reg_input.disabled = False
        
        show_material_model()
    

# %%%% [03-04-16] UPDATE MODEL PARAM ACCORDING OTHER TAG MINMAX
# Function to update the parameters of the Other material in MinMax model
def update_otherTag_parameters(change=None):
    global OtherTag_minmax_dropdown, model_type_dropdown, observer_enabled
    global model_widgets
    
    observer_enabled = False
    
    # Obtain the files of materials defined
    selected_files = [cb.description for cb in files_checkboxes_3]
    Other_Tag = OtherTag_minmax_dropdown.value
    
    # Search the file with the selected Other Tag
    for file in selected_files:
        if file.split('_')[1] == str(Other_Tag):
            model_of_file_selected = file.split('_')[2]
            # Example of value of model_of_file_selected = 'ConcreteCM.txt'
            # Delete the .txt strings to obtain the model
            model_of_file_selected = model_of_file_selected.split('.')[0]
            file_selected = file
            break
        
    # Update parameters of the model selected
    model_type_dropdown.options = [model_of_file_selected]
    model_type_dropdown.value = model_of_file_selected
    update_model_widgets()

    # Read the .txt files
    url_x = directory_3 + "/" + f"{file_selected}"
    
    # Read the .txt files and create a list with the data of the file
    with open(url_x, 'r') as file:
        model_args_prev = [line.strip() for line in file.readlines()]
    
    # Obtain the units of the model
    unit_model = model_args_prev[1]
    material_type = 'MinMax'
    # Assign the rest of the values to the variable model_args
    model_args = model_args_prev[2:]
    # Replace the [1] term of the list (MatTag), for a value that I want
    model_args[1] = str(MatTag_minmax_input.value)
    assign_values_to_model_args(model_args, unit_model, material_type)
    OtherTag_minmax_dropdown.value = Other_Tag
    show_material_model()
    
    # Disable all Text widgets within the VBox
    for widget in model_widgets.children:
        if isinstance(widget, Text):
            widget.disabled = True

    observer_enabled = True

# %%%% [03-04-17] SHOW_INSTRUCTIONS
# Function to show instructions
def show_instructions(change=None):
    code_params_output.value = """Instructions:
+ Define Strain Loading: Crea una archivo de texto con parametros para crear array de solicitaciones.
    Definir Strain Load:
        1. Presionar el boton Define para comenzar a definir una carga.
        2. Seleccionar una ID Load. Cuidar que este valor sea unico para cada secuencia.
        3. Seleccionar un tipo de carga: Monotonic, Cyclic.
        4. Si la solicitacion es del tipo Cyclic, seleccionar el tipo de ciclo.
        5. Presionar el boton show para visualizar la carga en el grafico.
        6. Modifica los parametros de la carga 
        Nota 1: Puede visualizar las modificaciones en la grafica en tiempo real.
        7. Presionar el boton Save para guardar la carga.
        Nota 2: En el area Strain Loadings puede visualizar el archivo creado.
    Modificar Strain Load:
        1. En el area Strain Loadings, seleccione un archivo de texto.
        2. Presione el boton Edit para modificar la carga.
        3. Modifica los parametros de la carga.
        4. Presione el boton Save para guardar la carga.

+ Define Material Model: Crea un archivo de texto con parametros para definir un modelo de comportamiento.
    Definir Material Model:
        1. Presionar el boton Define Material Model para comenzar a definir el modelo.
        2. Seleccionar un Material Tag unico para cada modelo definido.
        3. Seleccionar el tipo de material.
        4. Seleccionar el modelo a emplear.
        5. Seleccionar las unidades a emplear en el modelo.
        7. Seleccionar un archivo de texto Strain Load para visualizar el comportamiento del material.
        8. Seleccione las unidades de la grafica.
        9. Presione el boton show para visualizar el comportamiento del material.
        10. Modificar los parametros del material.
        Nota 1: Puede visualizar las modificaciones en la grafica en tiempo real.
        11. Presionar el boton Save para guardar el modelo.
        Nota 2: En el area Material Model puede visualizar el archivo creado.
    Modificar Material Model:
        1. En el area Material Model, seleccione un archivo de texto.
        2. Presione el boton Edit para modificar el modelo.
        3. Modifica los parametros del material.
        4. Presione el boton Save para guardar el modelo.

+ Define Responses: Crea una archivo de texto con los parametros de la solicitacion, del material y almacena la respuesta.
    Definir Response:
        1. Mientras se visualiza el comportamiento de los materiales presionar definir response.
    Visualizar Response:
        A. En el area Responses, seleccione un archivo de texto.
        B. Presione el boton graphic/cyclic graphic/cyclic video para visualizar la respuesta.
        C. Si lo desea puede modificar las unidades de la grafica.
        Nota 1: Puede visualizar las graficas de mas de un archivo response a la vez.
    Visualizar Code:
        A. En el area Responses, seleccione un archivo de texto.
        B. Presione el boton Code para visualizar el codigo del archivo seleccionado.
        Nota 2: Puede visualizar el codigo de mas de un archivo response a la vez.
"""


# %% [04] WIDGETS
# Dimension para ingresar datos numericos.
layout_var_1 = widgets.Layout(width='195px')
layout_var_2 = widgets.Layout(width='175px')
layout_var = widgets.Layout(width='185px')

# %%% [04-00] Dropdown
# Interactive widget to choose model type Concrete/Steel
material_type_dropdown = Dropdown(
    options=['Concrete', 'Steel', 'MinMax', 'User defined'],
    value='Concrete',
    description='Mat. Type:',
    disabled=True,
    layout=layout_var_1
)

# Interactive widget for model
model_type_dropdown = Dropdown(
    options=['ConcreteCM', 'Concrete07'],
    value='ConcreteCM',
    description='Model:',
    disabled=True,
    layout=layout_var_1
)

# Interactive widget for type of deformation
load_type_dropdown = Dropdown(
    options=['monotonic', 'cyclic'],
    value='cyclic',
    description='Load type:',
    disabled=True,
    layout=layout_var_1
)

# Interactive widget for type of deformation cyclic
cyclic_type_dropdown = Dropdown(
    options=['compression', 'combined', 'traction'],
    value='compression',
    description='Type:',
    disabled=True,
    layout=layout_var_1
)

# Interactive widget for units
unit_dropdown = Dropdown(
    options=['kgf/cm**2', 'tonf/m**2', 'ksi', 'psi', 'Pa', 'MPa'],
    value='kgf/cm**2',
    description='Units:',
    disabled=True,
    layout=layout_var_1
)

# Dropdown widget for graphic unit
graphic_unit_dropdown = Dropdown(
    options=['-', 'kgf/cm**2', 'tonf/m**2', 'ksi', 'psi', 'Pa', 'MPa'],
    value='kgf/cm**2',
    description='Graphic Unit:',
    disabled=True,
    layout=layout_var_1
)

# Dropdown widget for strain loading
strain_loading_dropdown = Dropdown(
    options = ['-'],
    value = '-',
    description = 'Strain Load:',
    disabled = True,
    layout = layout_var_1
)

# %%% [04-01] Text - IntText
# Interactive widgets for material tag & ID cyclic load
MatTag_input = IntText(value=1, disabled=True, description='Material Tag:', layout=layout_var_1)
id_cyclic_load_input = IntText(value=1, disabled=True, description='ID Load:', layout=layout_var_1)

# Interactive widgets for deformation monotonic
delta_e = Text(value='0.0001', description='delta_e:', continuous_update=False, layout=layout_var_2)
e_max_c = Text(value='-0.006', description='e_max_c:', continuous_update=False, layout=layout_var_2)
e_max_t = Text(value='0.0005', description='e_max_t:', continuous_update=False, layout=layout_var_2)

# Interactive widgets for deformation cyclic compression
e_max_c_1 = Text(value='-0.0010', description='e_max_c1:', continuous_update=False, layout=layout_var_2)
e_max_c_2 = Text(value='-0.0020', description='e_max_c2:', continuous_update=False, layout=layout_var_2)
e_max_c_3 = Text(value='-0.0030', description='e_max_c3', continuous_update=False, layout=layout_var_2)
e_max_c_4 = Text(value='-0.0040', description='e_max_c4:', continuous_update=False, layout=layout_var_2)
e_max_c_5 = Text(value='-0.0050', description='e_max_c5:', continuous_update=False, layout=layout_var_2)

# Interactive widgets for deformation cyclic traccion
e_max_t_1 = Text(value=' 0.00005', description='e_max_t1:', continuous_update=False, layout=layout_var_2)
e_max_t_2 = Text(value=' 0.00010', description='e_max_t2:', continuous_update=False, layout=layout_var_2)
e_max_t_3 = Text(value=' 0.00015', description='e_max_t3:', continuous_update=False, layout=layout_var_2)
e_max_t_4 = Text(value=' 0.00020', description='e_max_t4:', continuous_update=False, layout=layout_var_2)
e_max_t_5 = Text(value=' 0.00025', description='e_max_t5:', continuous_update=False, layout=layout_var_2)

# Interactive widgets for deformation cyclic combined
pulso_1 = Text(value='1', description='#Peaks 1:', continuous_update=False, layout=layout_var_2)
pulso_2 = Text(value='1', description='#Peaks 2:', continuous_update=False, layout=layout_var_2)
pulso_3 = Text(value='1', description='#Peaks 3:', continuous_update=False, layout=layout_var_2)
pulso_4 = Text(value='1', description='#Peaks 4:', continuous_update=False, layout=layout_var_2)
pulso_5 = Text(value='1', description='#Peaks 5:', continuous_update=False, layout=layout_var_2)

# Widgets for regularization of concrete models
fc_reg_input = Text(value='-250.0', description='fc:', continuous_update=False, layout=layout_var)
ec_reg_input = Text(value='-0.002', description='ec:', continuous_update=False, layout=layout_var)
Ec_reg_input = Text(value='238751.9633', description='Ec:', continuous_update=False, layout=layout_var)
fr_reg_input = Text(value='50', description='fr:', continuous_update=False, layout=layout_var)
Gfc_cc_input = Text(value='89.2898366141732', description='Gfc_cc:', continuous_update=False, layout=layout_var)
L_reg_input = Text(value='100', description='L:', continuous_update=False, layout=layout_var)

# Widgets for MinMax material model
MatTag_minmax_input = IntText(value=1, description='Material Tag:', layout=layout_var)
OtherTag_minmax_dropdown = Dropdown(options = ['-'], value = '-', description = 'Other Tag:', disabled = False, layout = layout_var)
minStrain_input = Text(value='-1.0e16', description='minStrain:', continuous_update=False, layout=layout_var)
maxStrain_input = Text(value='1.0e16', description='maxStrain:', continuous_update=False, layout=layout_var)

# Extra widgets for different model types
# ConcreteCM
fpcc_input = Text(value='-250.0', description="fpcc:", continuous_update=False, layout=layout_var)
epcc_input = Text(value='-0.002', description="epcc:", continuous_update=False, layout=layout_var)
Ec_input = Text(value='238751.9633', description="Ec:", continuous_update=False, layout=layout_var)
rc_input = Text(value='7', description="rc:", continuous_update=False, layout=layout_var)
xcrn_input = Text(value='1.05', description="xcrn:", continuous_update=False, layout=layout_var)
ft_input = Text(value='34.78', description="ft:", continuous_update=False, layout=layout_var)
et_input = Text(value='0.0001', description="et:", continuous_update=False, layout=layout_var)
rt_input = Text(value='7', description="rt:", continuous_update=False, layout=layout_var)
xcrp_input = Text(value='10000', description="xcrp:", continuous_update=False, layout=layout_var)
GapClose_dropdown = Text(value='-GapClose', description="-GapClose:", continuous_update=False, layout=layout_var)
GapClose_input = Text(value='1', description='GapClose:', continuous_update=False, layout=layout_var)
# Concrete07
fc_input = Text(value='-250.0', description="fc:", continuous_update=False, layout=layout_var)
epsc_input = Text(value='-0.002', description="epsc:", continuous_update=False, layout=layout_var)
xp_input = Text(value='10000', description="xp:", continuous_update=False, layout=layout_var)
xn_input = Text(value='1.05', description="xn:", continuous_update=False, layout=layout_var)
r_input = Text(value='7', description="r:", continuous_update=False, layout=layout_var)
# SteelMPF
fyp_input = Text(value='4200.0', description="fyp:", continuous_update=False, layout=layout_var)
fyn_input = Text(value='4200.0', description="fyn:", continuous_update=False, layout=layout_var)
E0_input = Text(value='2100000', description="E0:", continuous_update=False, layout=layout_var)
bp_input = Text(value='0.02', description="bp:", continuous_update=False, layout=layout_var)
bn_input = Text(value='0.02', description="bn:", continuous_update=False, layout=layout_var)
R0_input = Text(value='20', description="R0:", continuous_update=False, layout=layout_var)
cR1_input = Text(value='0.925', description="cR1:", continuous_update=False, layout=layout_var)
cR2_input = Text(value='0.0015', description="cR2:", continuous_update=False, layout=layout_var)
a1_input = Text(value='0.0', description="a1:", continuous_update=False, layout=layout_var)
a2_input = Text(value='1.0', description="a2:", continuous_update=False, layout=layout_var)
a3_input = Text(value='0.0', description="a3:", continuous_update=False, layout=layout_var)
a4_input = Text(value='1.0', description="a4:", continuous_update=False, layout=layout_var)
# Steel02
# uniaxialMaterial('Steel02', matTag, Fy, E0, b, *params, a1=a2*Fy/E0, a2=1.0, a3=a4*Fy/E0, a4=1.0, sigInit=0.0)
# Inputs already defined: MatTag_input
Fy_Steel02_input = Text(value='4200.0', description="Fy:", continuous_update=False, layout=layout_var)
E0_Steel02_input = Text(value='2100000', description="E0:", continuous_update=False, layout=layout_var)
b_Steel02_input = Text(value='0.02', description="b:", continuous_update=False, layout=layout_var)
R0_Steel02_input = Text(value='20', description="R0:", continuous_update=False, layout=layout_var)
cR1_Steel02_input = Text(value='0.925', description="cR1:", continuous_update=False, layout=layout_var)
cR2_Steel02_input = Text(value='0.15', description="cR2:", continuous_update=False, layout=layout_var)
a1_Steel02_input = Text(value='0.0', description="a1:", continuous_update=False, layout=layout_var)
a2_Steel02_input = Text(value='1.0', description="a2:", continuous_update=False, layout=layout_var)
a3_Steel02_input = Text(value='0.0', description="a3:", continuous_update=False, layout=layout_var)
a4_Steel02_input = Text(value='1.0', description="a4:", continuous_update=False, layout=layout_var)
sigInit_Steel02_input = Text(value='0.0', description="sigInit:", continuous_update=False, layout=layout_var)
# Steel01
# uniaxialMaterial('Steel01', matTag, Fy, E0, b, a1, a2, a3, a4)
# Inputs already defined: MatTag_input
Fy_Steel01_input = Text(value='4200.0', description="Fy:", continuous_update=False, layout=layout_var)
E0_Steel01_input = Text(value='2100000', description="E0:", continuous_update=False, layout=layout_var)
b_Steel01_input = Text(value='0.02', description="b:", continuous_update=False, layout=layout_var)
a1_Steel01_input = Text(value='0.0', description="a1:", continuous_update=False, layout=layout_var)
a2_Steel01_input = Text(value='1.0', description="a2:", continuous_update=False, layout=layout_var)
a3_Steel01_input = Text(value='0.0', description="a3:", continuous_update=False, layout=layout_var)
a4_Steel01_input = Text(value='1.0', description="a4:", continuous_update=False, layout=layout_var)
# Steel4
# uniaxialMaterial('Steel4', matTag, Fy, E0, '-asym', '-kin', b_k, *params, b_kc, R_0c, r_1c, r_2c, '-iso', b_i, rho_i, b_l, R_i, l_yp, b_ic, rho_ic, b_lc, R_ic, '-ult', f_u, R_u, f_uc, R_uc, '-init', sig_init, '-mem', cycNum)
# Inputs already defined: MatTag_input
Fy_Steel4_input = Text(value='4200.0', description="Fy:", continuous_update=False, layout=layout_var)
E0_Steel4_input = Text(value='2100000', description="E0:", continuous_update=False, layout=layout_var)
b_k_Steel4_input = Text(value='0.05', description="b_k:", continuous_update=False, layout=layout_var)
R0_Steel4_input = Text(value='20', description="R0:", continuous_update=False, layout=layout_var)
r1_Steel4_input = Text(value='0.9', description="r1:", continuous_update=False, layout=layout_var)
r2_Steel4_input = Text(value='0.15', description="r2:", continuous_update=False, layout=layout_var)
b_kc_Steel4_input = Text(value='0.05', description="b_kc:", continuous_update=False, layout=layout_var)
R0c_Steel4_input = Text(value='20', description="R0c:", continuous_update=False, layout=layout_var)
r1c_Steel4_input = Text(value='0.90', description="r1c:", continuous_update=False, layout=layout_var)
r2c_Steel4_input = Text(value='0.15', description="r2c:", continuous_update=False, layout=layout_var)
b_i_Steel4_input = Text(value='0.2', description="b_i:", continuous_update=False, layout=layout_var)
rho_i_Steel4_input = Text(value='0.2', description="rho_i:", continuous_update=False, layout=layout_var)
b_I_Steel4_input = Text(value='0.1', description="b_I:", continuous_update=False, layout=layout_var)
R_i_Steel4_input = Text(value='20', description="R_i:", continuous_update=False, layout=layout_var)
I_yp_Steel4_input = Text(value='2.5', description="I_yp:", continuous_update=False, layout=layout_var)
b_ic_Steel4_input = Text(value='0.2', description="b_ic:", continuous_update=False, layout=layout_var)
rho_ic_Steel4_input = Text(value='0.2', description="rho_ic:", continuous_update=False, layout=layout_var)
b_Ic_Steel4_input = Text(value='0.1', description="b_Ic:", continuous_update=False, layout=layout_var)
R_ic_Steel4_input = Text(value='20', description="R_ic:", continuous_update=False, layout=layout_var)
f_u_Steel4_input = Text(value='6300.0', description="f_u:", continuous_update=False, layout=layout_var)
R_u_Steel4_input = Text(value='20', description="R_u:", continuous_update=False, layout=layout_var)
f_uc_Steel4_input = Text(value='6300.0', description="f_uc:", continuous_update=False, layout=layout_var)
R_uc_Steel4_input = Text(value='20', description="R_uc:", continuous_update=False, layout=layout_var)
sig_init_Steel4_input = Text(value='0.0', description="sig_init:", continuous_update=False, layout=layout_var)
cycNum_Steel4_input = Text(value='0', description="cycNum:", continuous_update=False, layout=layout_var)

# Extra widgets for user defined materials
# Saatcioglu(1992)
fco_input = Text(value='250.0', description="fco:", continuous_update=False, layout=layout_var)
fl_input = Text(value='0.0001', description="fle:", continuous_update=False, layout=layout_var)
e01_input = Text(value='0.002', description="e01:", continuous_update=False, layout=layout_var)
rho_input = Text(value='0.00001', description="rho:", continuous_update=False, layout=layout_var)
e085_input = Text(value='0.0038', description="e085:", continuous_update=False, layout=layout_var)
# Mander(1988)
CSR_input = Text(value='1.15', description="CSR:", continuous_update=False, layout=layout_var)
eco_input = Text(value='0.002', description="eco:", continuous_update=False, layout=layout_var)
# Belarbi(1994)
f_cr_input = Text(value='20.0', description="fcr:", continuous_update=False, layout=layout_var)
eps_cr_input = Text(value='0.00008', description="eps_cr:", continuous_update=False, layout=layout_var)
Ecr_input = Text(value='261148.919', description="Ecr:", continuous_update=False, layout=layout_var)


# %%% [04-02] ZIP WDGT
input_widgets = VBox(layout=widgets.Layout(width='230px', height='675px', padding='0px'))
# This group of widgets is update using update_model_widgets() & update_defo_widgets()
model_widgets = VBox(layout=widgets.Layout(width='200px', height='435px', padding='0px'))  # model_widgets = VBox(layout=widgets.Layout(width='200px', height='665px', padding='0px'))
regularization_widgets = VBox(layout=widgets.Layout(width='200px', height='230px', padding='0px'))  # Textarea(value='', layout=widgets.Layout(width='200px', height='170px'))


# %%% [04-03] OBSERVE DROPDOWNS
# Observe changes in the dropdowns and modify the options in related widgets
material_type_dropdown.observe(update_model_type_dropdown, names='value')
model_type_dropdown.observe(update_model_widgets, names='value')
graphic_unit_dropdown.observe(update_unit_options, names='value')
graphic_unit_dropdown.observe(show_material_model, names='value')
load_type_dropdown.observe(update_cyclic_type_dropdown, names='value')
cyclic_type_dropdown.observe(update_defo_widgets, names='value')
unit_dropdown.observe(update_model_widgets, names='value')


# %%% [04-04] BUTTONS
# Button to see instructions in user defined materials.
see_instruction_button_layout = widgets.Layout(width='185px')
see_instruction_button = widgets.Button(description='Show Instructions', layout=see_instruction_button_layout)
see_instruction_button.on_click(see_instruction)
# Button to add response.
add_file_button_layout = widgets.Layout(width='203px', margin="0px 0px 3px 2px")
add_file_button = widgets.Button(description='Define Response', layout=add_file_button_layout)
add_file_button.disabled = True
add_file_button.on_click(add_response)
# Button to show graphic.
show_graphic_button_layout = widgets.Layout(width='107px')
show_graphic_button = widgets.Button(description='Show Graphic', layout=show_graphic_button_layout)
show_graphic_button.disabled = True
show_graphic_button.on_click(show_graphic)
# Button to show code.
show_code_button_layout = widgets.Layout(width='92px')
show_code_button = widgets.Button(description='Show Code', layout=show_code_button_layout)
show_code_button.disabled = True
show_code_button.on_click(show_code)
# Button to show cyclic graphic.
show_cyclic_graphic_button_layout = widgets.Layout(width='107px')
show_cyclic_graphic_button = widgets.Button(description='Cyclic Graphic', layout=show_cyclic_graphic_button_layout)
show_cyclic_graphic_button.disabled = True
show_cyclic_graphic_button.on_click(show_cyclic_graphic)
# Button to show cyclic video.
show_cyclic_video_button_layout = widgets.Layout(width='92px')
show_cyclic_video_button = widgets.Button(description='Cyclic Video', layout=show_cyclic_video_button_layout)
show_cyclic_video_button.disabled = True
show_cyclic_video_button.on_click(show_cyclic_video)
# Button to delete file.
delete_file_button_layout = widgets.Layout(width='130px')
delete_file_button = widgets.Button(description='Delete File', layout=delete_file_button_layout)
delete_file_button.disabled = False
delete_file_button.on_click(delete_file)
# Button to delete all.
delete_all_button_layout = widgets.Layout(width='145px')
delete_all_button = widgets.Button(description='Delete All', layout=delete_all_button_layout)
delete_all_button.disabled = False
delete_all_button.on_click(delete_all)
# Button to refresh files.
refresh_files_button_layout = widgets.Layout(width='130px')
refresh_files_button = widgets.Button(description='Refresh Files', layout=refresh_files_button_layout)
refresh_files_button.disabled = False
refresh_files_button.on_click(refresh_files)
# Button to define cyclic strain load
define_cyclic_load_button_layout = widgets.Layout(width='65px')
define_cyclic_load_button = widgets.Button(layout=define_cyclic_load_button_layout)
define_cyclic_load_button.description = 'Define'
define_cyclic_load_button.on_click(define_cyclic_load)
# Button to display cyclic strain load
show_cyclic_load_button_layout = widgets.Layout(width='65px')
show_cyclic_load_button = widgets.Button(layout=show_cyclic_load_button_layout)
show_cyclic_load_button.description = '-'
show_cyclic_load_button.disabled = True
show_cyclic_load_button.on_click(show_cyclic_load)
# Button to modify the cyclic strain load from a file
modify_cyclic_load_button_layout = widgets.Layout(width='65px')
modify_cyclic_load_button = widgets.Button(layout=modify_cyclic_load_button_layout)
modify_cyclic_load_button.description = 'Edit'
modify_cyclic_load_button.disabled = False
modify_cyclic_load_button.on_click(modify_cyclic_load)
# Button to define a material model
define_material_model_button_layout = widgets.Layout(width='65px')
define_material_model_button = widgets.Button(layout=define_material_model_button_layout)
define_material_model_button.description = 'Define'
define_material_model_button.on_click(define_material_model)
# Burron to display material model
show_material_model_button_layout = widgets.Layout(width='65px')
show_material_model_button = widgets.Button(layout=show_material_model_button_layout)
show_material_model_button.description = '-'
show_material_model_button.disabled = True
show_material_model_button.on_click(show_material_model)
# Button to modify the material model from a file
modify_material_model_button_layout = widgets.Layout(width='65px')
modify_material_model_button = widgets.Button(layout=modify_material_model_button_layout)
modify_material_model_button.description = 'Edit'
modify_material_model_button.disabled = False
modify_material_model_button.on_click(modify_material_model)
# Button to see instructions of the GUI
instructions_button_layout = widgets.Layout(width='205px', margin='0 0 9px 0')
instructions_button = widgets.Button(description='Show Instructions', layout=instructions_button_layout)
instructions_button.on_click(show_instructions)
# Button to the regularization of the concrete models
regularization_button_layout = widgets.Layout(width='185px')
regularization_button = widgets.Button(description='Post-peak Regularization', layout=regularization_button_layout)
regularization_button.on_click(regularize_material)

# Button to the regularization of the concrete models
MinMax_button_layout = widgets.Layout(width='185px')
MinMax_button = widgets.Button(description='Load Other Mat Parameters', layout=MinMax_button_layout)
MinMax_button.on_click(update_otherTag_parameters)


# %%% [04-05] SET UP INITIAL WIDGETS
# All buttons and Widgets: List with buttons for disabled and enabled them faster
all_buttons_and_widgets_list = [
    see_instruction_button, add_file_button, show_graphic_button, show_code_button, 
    show_cyclic_graphic_button, show_cyclic_video_button, delete_file_button, delete_all_button, 
    refresh_files_button, define_cyclic_load_button, show_cyclic_load_button, modify_cyclic_load_button,
    define_material_model_button, show_material_model_button, modify_material_model_button,
    model_type_dropdown, material_type_dropdown, unit_dropdown, graphic_unit_dropdown, strain_loading_dropdown,
    load_type_dropdown, cyclic_type_dropdown, MatTag_input, id_cyclic_load_input]

# Buttons for initial state
buttons_initial_state = [see_instruction_button, show_graphic_button, show_code_button,
                         show_cyclic_graphic_button, show_cyclic_video_button, delete_file_button, delete_all_button,
                         refresh_files_button, define_cyclic_load_button, modify_cyclic_load_button,
                         define_material_model_button, modify_material_model_button]

# Enable initial widgets
for widget in all_buttons_and_widgets_list:
    if widget in buttons_initial_state:
        widget.disabled = False
    else:
        widget.disabled = True

# %%% [04-06] TEXTAREA
# Display section code parameter
code_params_output = Textarea(value='', layout=widgets.Layout(width='664px', height='269px'))  # '660px'
# Display files ploted
graph_output = Textarea(value='', layout=widgets.Layout(width='664px', height='30px'))

# %%% [04-07] OUTPUT
# Output widget to contain the plot (text to try select .txt files)
layout_rigth = widgets.Layout(width='664px', height='332px', margin="0 0 0 3px")
out = Output(layout=layout_rigth)  # Output

# %%% [04-08] CHECKBOX

# %%%% [04-08-00] STRAIN_STRESS_FILES
# Directory to be listed
directory = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial'
# Create Checkboxes for the files in the directory
files_checkboxes = list_files_with_checkboxes(directory)
# Display checkboxes
files_checkboxes_box = VBox(layout=widgets.Layout(width='357px', height='300px'))
files_checkboxes_box.children = files_checkboxes

# %%%% [04-08-01] STRAIN_LOAD_FILES
# Directory to be listed
directory_2 = 'C_GUI02_uniaxialMaterial/C_GUI02_StrainLoad'
files_checkboxes_2 = list_files_with_checkboxes(directory_2)
# Display checkboxes
files_checkboxes_box_2 = VBox(layout=widgets.Layout(width='357px', height='300px'))
files_checkboxes_box_2.children = files_checkboxes_2

# %%%% [04-08-02] MATERIAL_MODEL_FILES
# Directory to be listed
directory_3 = 'C_GUI02_uniaxialMaterial/C_GUI02_MaterialModel'
files_checkboxes_3 = list_files_with_checkboxes(directory_3)
# Display checkboxes
files_checkboxes_box_3 = VBox(layout=widgets.Layout(width='357px', height='300px'))
files_checkboxes_box_3.children = files_checkboxes_3

# %%% [04-09] MATH IN WIDGETS & DYNAMIC GRAPHICS
# Widgets in the GUI
widgets_list = [delta_e, e_max_c, e_max_t,
    e_max_c_1, e_max_c_2, e_max_c_3, e_max_c_4, e_max_c_5,
    e_max_t_1, e_max_t_2, e_max_t_3, e_max_t_4, e_max_t_5,
    pulso_1, pulso_2, pulso_3, pulso_4, pulso_5,
    fpcc_input, epcc_input, Ec_input, rc_input, xcrn_input, ft_input, et_input,
    rt_input, xcrp_input,
    fc_input, epsc_input, xp_input, xn_input, r_input,
    fyp_input, fyn_input, E0_input, bp_input, bn_input, R0_input, cR1_input,
    cR2_input, a1_input, a2_input, a3_input, a4_input,
    fco_input, fl_input, e01_input, rho_input, e085_input,
    CSR_input, eco_input,
    fc_reg_input, ec_reg_input, Ec_reg_input, fr_reg_input, Gfc_cc_input, L_reg_input,
    minStrain_input, maxStrain_input,
    f_cr_input, eps_cr_input, Ecr_input,
    Fy_Steel02_input, E0_Steel02_input, b_Steel02_input, R0_Steel02_input, cR1_Steel02_input, cR2_Steel02_input,
    a1_Steel02_input, a2_Steel02_input, a3_Steel02_input, a4_Steel02_input, sigInit_Steel02_input,
    Fy_Steel01_input, E0_Steel01_input, b_Steel01_input, a1_Steel01_input, a2_Steel01_input, a3_Steel01_input, a4_Steel01_input,
    Fy_Steel4_input, E0_Steel4_input, b_k_Steel4_input, R0_Steel4_input, r1_Steel4_input, r2_Steel4_input,
    b_kc_Steel4_input, R0c_Steel4_input, r1c_Steel4_input, r2c_Steel4_input, b_i_Steel4_input, rho_i_Steel4_input,
    b_I_Steel4_input, R_i_Steel4_input, I_yp_Steel4_input, b_ic_Steel4_input, rho_ic_Steel4_input, b_Ic_Steel4_input,
    R_ic_Steel4_input, f_u_Steel4_input, R_u_Steel4_input, f_uc_Steel4_input, R_uc_Steel4_input, sig_init_Steel4_input,
    cycNum_Steel4_input]

widgets_graphic_strain = [delta_e, e_max_c, 
                   e_max_t, e_max_c_1, e_max_c_2, e_max_c_3, e_max_c_4, e_max_c_5, 
                   e_max_t_1, e_max_t_2, e_max_t_3, e_max_t_4, e_max_t_5, pulso_1, 
                   pulso_2, pulso_3, pulso_4, pulso_5]

widgets_graphic_material = [fpcc_input, epcc_input, Ec_input, rc_input, xcrn_input, ft_input, et_input,
                            rt_input, xcrp_input,
                            fc_input, epsc_input, xp_input, xn_input, r_input,
                            fyp_input, fyn_input, E0_input, bp_input, bn_input, R0_input, cR1_input,
                            cR2_input, a1_input, a2_input, a3_input, a4_input,
                            fco_input, fl_input, e01_input, rho_input, e085_input,
                            CSR_input, eco_input,
                            minStrain_input, maxStrain_input,
                            f_cr_input, eps_cr_input, Ecr_input,
                            Fy_Steel02_input, E0_Steel02_input, b_Steel02_input, R0_Steel02_input, cR1_Steel02_input, cR2_Steel02_input,
                            a1_Steel02_input, a2_Steel02_input, a3_Steel02_input, a4_Steel02_input, sigInit_Steel02_input,
                            Fy_Steel01_input, E0_Steel01_input, b_Steel01_input, a1_Steel01_input, a2_Steel01_input, a3_Steel01_input, a4_Steel01_input,
                            Fy_Steel4_input, E0_Steel4_input, b_k_Steel4_input, R0_Steel4_input, r1_Steel4_input, r2_Steel4_input,
                            b_kc_Steel4_input, R0c_Steel4_input, r1c_Steel4_input, r2c_Steel4_input, b_i_Steel4_input, rho_i_Steel4_input,
                            b_I_Steel4_input, R_i_Steel4_input, I_yp_Steel4_input, b_ic_Steel4_input, rho_ic_Steel4_input, b_Ic_Steel4_input,
                            R_ic_Steel4_input, f_u_Steel4_input, R_u_Steel4_input, f_uc_Steel4_input, R_uc_Steel4_input, sig_init_Steel4_input,
                            cycNum_Steel4_input]

widgets_regularization = [Gfc_cc_input, L_reg_input]

# Dropdowns in the GUI that affect the graphic
dropdowns_list = [load_type_dropdown, cyclic_type_dropdown, unit_dropdown, 
                  graphic_unit_dropdown, material_type_dropdown, 
                  model_type_dropdown, strain_loading_dropdown]

dropdowns_graphic_strain = [cyclic_type_dropdown]

dropdowns_graphic_material = [unit_dropdown, graphic_unit_dropdown, 
                              model_type_dropdown, strain_loading_dropdown]

# Helper function to observe the widgets with mathematical expressions 
def observe_widget(widget_x):
    def handler(change):
        if observer_enabled:
            widget_x.value = str(eval(change['new']))
    widget_x.observe(handler, names='value')


# Helper function to observe the widgets for the strain loading graphic
def observe_widget_graphic_strain(widget_x):
    def handler_2(change):
        if observer_enabled:
            # Check if 'change['new']' is a mathematical expression or already a number
            try:
                # Attempt to convert 'change['new']' to float
                new_value = float(change['new'])
                # If successful, it's already a number, so no need to eval
                is_number = True
            except ValueError:
                # If conversion fails, it's not a simple number
                is_number = False

            # Only graph if 'change['new']' is already a number:
            if is_number:
                if define_cyclic_load_button.description == 'Save':
                    show_cyclic_load()
            # Only evaluate if 'change['new']' is not already a number
            if not is_number:
                widget_x.value = str(eval(change['new']))
    widget_x.observe(handler_2, names='value')


# Helper function to observe the widgets for the material model graphic
def observe_widget_graphic_material_model(widget_x):
    def handler_3(change):
        if observer_enabled:
            # Check if 'change['new']' is a mathematical expression or already a number
            try:
                # Attempt to convert 'change['new']' to float
                new_value = float(change['new'])
                # If successful, it's already a number, so no need to eval
                is_number = True
            except ValueError:
                # If conversion fails, it's not a simple number
                is_number = False
                
            # Only graph if 'change['new']' is already a number:
            if is_number:
                if define_material_model_button.description == 'Save':
                    show_material_model()
            # Only evaluate if 'change['new']' is not already a number
            if not is_number:
                widget_x.value = str(eval(change['new']))
    widget_x.observe(handler_3, names='value')


# Helper function to observe the dropdowns for the strain loading graphic
def observe_dropdown_graphic_strain(dropdown_x):
    def handler_4(change):
        if observer_enabled:
            if define_cyclic_load_button.description == 'Save':
                show_cyclic_load()
    dropdown_x.observe(handler_4, names='value')


# Helper function to observe the dropdowns for the material model graphic
def observe_dropdown_graphic_material_model(dropdown_x):
    def handler_5(change):
        if observer_enabled:
            if define_material_model_button.description == 'Save':
                show_material_model()
    dropdown_x.observe(handler_5, names='value')


# Apply the observation to all widgets
for widget in widgets_list:
    if widget in widgets_graphic_strain:
        observe_widget_graphic_strain(widget)
    elif widget in widgets_graphic_material:
        observe_widget_graphic_material_model(widget)
    else:
        observe_widget(widget)


# Apply the observation to all dropdowns
for dropdown in dropdowns_list:
    if dropdown in dropdowns_graphic_strain:
        observe_dropdown_graphic_strain(dropdown)
    elif dropdown in dropdowns_graphic_material:
        observe_dropdown_graphic_material_model(dropdown)
    else:
        pass

# Function to update the units in widgets when unit_dropdown changes

# Store the previous unit
actual_units = 'kgf/cm**2'
last_units = 'kgf/cm**2'
actual_units_2 = 'kgf/cm'
last_units_2 = 'kgf/cm'
actual_units_3 = 'cm'
last_units_3 = 'cm'

def update_unit_options(change=None):
    global actual_units, last_units, observer_enabled
    global actual_units_2, last_units_2, actual_units_3, last_units_3
    global unit_factors_new, unit_factors_new_2, unit_factors_new_3
    global description_units

    # Update actual_units
    actual_units = unit_dropdown.value
    actual_units_2 = description_units[unit_dropdown.value]['Unit Gfc_cc_input']
    actual_units_3 = description_units[unit_dropdown.value]['Unit L_reg_input']
    
    # If actual_units is different from last_units, update the widgets
    if actual_units != last_units:
        # Don't update the graphic
        observer_enabled = False
        
        # Update the widgets
        for widget in widgets_list:
            if widget in widgets_regularization:
                if 'Gf' in widget.description:
                    widget.value = str(eval(widget.value)*unit_factors_new_2[actual_units_2][last_units_2])
                if 'L' in widget.description:
                    widget.value = str(eval(widget.value)*unit_factors_new_3[actual_units_3][last_units_3])
            
            # Check in the description of the widget if it contains unit.
            # For that, search if it has []. The unit is within the brackets.
            # This function because all the parameters are in the same units. (stress)
            elif '[' in widget.description:
                # How the element have units, apply the conversion.
                widget.value = str(eval(widget.value)*unit_factors_new[actual_units][last_units])
                
        # Update the last_units
        last_units = actual_units
        last_units_2 = actual_units_2
        last_units_3 = actual_units_3
        
        # Enable the observer
        observer_enabled = True
        
        # Update the graphic
        show_material_model()
    
    return
          
# Observe change in the unit dropdown
unit_dropdown.observe(update_unit_options, names='value')
      

# %%% [04-10] UPDATE DROPDOWN STRAIN LOADING GRAPHIC  
# Function to update the dropdown of strain loading
def update_strain_loading_dropdown(change=None):
    global strain_loading_dropdown, observer_enabled
    if observer_enabled:
        # Obtain the selected file
        selected_files = [cb.description for cb in files_checkboxes_2]
        selected_files.insert(0, '-')
        options_strain_load = selected_files
        strain_loading_dropdown.options = options_strain_load
        strain_loading_dropdown.value = '-'

# Observe change in the definition of the cyclic load
define_material_model_button.on_click(update_strain_loading_dropdown)
modify_material_model_button.on_click(update_strain_loading_dropdown)


# %%% [04-11] UPDATE DROPDOWN OTHER TAG MINMAX
# Function to update the dropdown of other tag in MinMax material model
def update_otherTag_minmax_dropdown(change=None):
    global OtherTag_minmax_dropdown
    # Obtain the files of materials defined
    selected_files = [cb.description for cb in files_checkboxes_3]
    
    # Only use the files that the material is defined using opensees functions
    model_in_opensees = ['ConcreteCM', 'Concrete07', 'SteelMPF', 'Steel02', 'Steel01', 'Steel4']
    # the files are called: 'MatTag_2_ConcreteCM.txt', 'MatTag_3_Concrete07.txt', etc
    selected_files = [file for file in selected_files if file.split('_')[2].split('.')[0] in model_in_opensees]
    
    # Split strings of files in the character '_' and take the MatTag availables
    selected_files = [file.split('_')[1] for file in selected_files]
    selected_files.insert(0, '-')
    options_otherTag = selected_files
    OtherTag_minmax_dropdown.options = options_otherTag

def observer_update_otherTag_minmax_dropdown(change=None):
    global observer_enabled
    if observer_enabled:
        update_otherTag_minmax_dropdown()
        
# Observe change in the definition of the cyclic load
define_material_model_button.on_click(observer_update_otherTag_minmax_dropdown)
refresh_files_button.on_click(observer_update_otherTag_minmax_dropdown)

# %%% [04-12] UPDATE TAG MATERIAL MINMAX
# Function to update the tag of the material in MinMax material model
def update_MatTag_minmax(change=None):
    global observer_enabled
    update_otherTag_parameters()

def observer_update_MatTag_minmax(change=None):
    global observer_enabled
    if observer_enabled:
        update_MatTag_minmax()

# Observe change in the material tag of the MinMax material model
MatTag_minmax_input.observe(observer_update_MatTag_minmax, names='value')

# %% [05] LAYOUT
# Layout of the interface

# %%% [05-00] TEXT
# title = widgets.Label("Fiber Section Opensees", layout=widgets.Layout(display="flex", justify_content="flex-start"))
title = widgets.HTML(value="<b>uniaxialMaterial - Openseespy</b>",
                     layout=widgets.Layout(width='320px', display="flex", justify_content="center", margin="0px 0px 13px 0px"))  #
title.style.font_size = '22px'
text_checkbox_stress_strain = widgets.HTML(value="Responses:", layout=widgets.Layout(width='130px', margin="9px 0 0 2px"))
text_checkbox_stress_strain.style.font_size = '14px'
text_checkbox_strain_load = widgets.HTML(value="Strain Loadings:", layout=widgets.Layout(width='130px', margin="9px 0 0 2px"))
text_checkbox_strain_load.style.font_size = '14px'
text_checkbox_material_model = widgets.HTML(value="Material Models:", layout=widgets.Layout(width='130px', margin="9px 0 0 2px"))
text_checkbox_material_model.style.font_size = '14px'
text4 = widgets.HTML(value="Image Information:", layout=widgets.Layout(width='249px', margin="53px 0 0 2px"))
text4.style.font_size = '14px'
text2 = widgets.HTML(value="Output Window:", layout=widgets.Layout(width='249px', margin="0px 0 0 2px"))
text2.style.font_size = '14px'
text3 = widgets.HTML(value="<i>GUI developed by M. Ortiz.<i>", layout=widgets.Layout(width='700px', margin="0 0 0 2px"))
text3.style.font_size = '14px'
text_graphic_unit = widgets.HTML(value="Select Graphic Properties:", layout=widgets.Layout(margin="0px 0 0 2px"))
text_graphic_unit.style.font_size = '14px'
text_input_material = widgets.HTML(value="Define Material Model:", layout=widgets.Layout(margin="0px 0 0 2px"))
text_input_material.style.font_size = '14px'
text_input_cyclic = widgets.HTML(value="Define Strain Loading:", layout=widgets.Layout(margin="0px 0 0 2px"))
text_input_cyclic.style.font_size = '14px'
text_input_responses = widgets.HTML(value="Response:", layout=widgets.Layout(margin="9px 0 0 2px"))
text_input_responses.style.font_size = '14px'
text_files = widgets.HTML(value="Files:", layout=widgets.Layout(margin="19px 0 0 2px"))
text_files.style.font_size = '14px'

# %%% [05-01] INTERFACE
button_strain_loadings_box = HBox([define_cyclic_load_button, show_cyclic_load_button, modify_cyclic_load_button], 
                                  layout=widgets.Layout(margin="3px 0 9px 0"))
button_material_model_box = HBox([define_material_model_button, show_material_model_button, modify_material_model_button],
                                 layout=widgets.Layout(margin="0px 0 9px 0"))
# layout=widgets.Layout(margin="3px 0 9px 0")

button_responses_box_1 = HBox([show_graphic_button, show_code_button])
button_responses_box_2 = HBox([show_cyclic_graphic_button, show_cyclic_video_button])
button_responses_box = VBox([button_responses_box_1, button_responses_box_2])

material_input_list = [instructions_button, text_input_cyclic, id_cyclic_load_input, load_type_dropdown, 
                      cyclic_type_dropdown, button_strain_loadings_box, text_input_material, MatTag_input,
                      material_type_dropdown, model_type_dropdown, unit_dropdown, button_material_model_box,
                      text_graphic_unit, graphic_unit_dropdown, strain_loading_dropdown,
                      text_input_responses, add_file_button, button_responses_box,
                      text_files]
input_widgets.children = material_input_list
model_widgets.children = []  # Initial empty

rigth_side = VBox([model_widgets, regularization_widgets])

title_input = HBox([title], layout=widgets.Layout(justify_content='center'))
upper_input = HBox([input_widgets, rigth_side])  # upper_input = HBox([input_widgets, model_widgets])
medium_input = HBox([refresh_files_button, delete_file_button, delete_all_button])
medium_input_4 = VBox([text_checkbox_strain_load, files_checkboxes_box_2])
medium_input_5 = VBox([text_checkbox_stress_strain, files_checkboxes_box])
medium_input_6 = VBox([text_checkbox_material_model, files_checkboxes_box_3])
left_side = VBox([title_input, upper_input, medium_input])
low_input = HBox([code_params_output])
rigth_side = VBox([out, text4, graph_output, text2, low_input])
interface = HBox([left_side, rigth_side])
low_checkbox = HBox([medium_input_4, medium_input_6, medium_input_5])
interface_A = VBox([interface, low_checkbox])
interface_B = VBox([interface_A, text3])
display(interface_B)

# %% [06] DEVELOPER
# Developer view
aux_view_developer = False
if aux_view_developer:
    # Layout programer
    programer_output = Textarea(value='', layout=widgets.Layout(width='1072px', height='380px'))  # 
    display(programer_output)

    # Function to display in GUI variable in certain line of code
    def GUI_info(Text_in_string, line_of_code,  variable):
        """
        Function to display in GUI certain line of code
        :param Text_in_string: Variable in string
        :param line_of_code: Line of code
        :param variable: Variable to display
        :return: None
        
        Calling using:
        current_line = inspect.currentframe().f_lineno
        GUI_info('load_args = ', current_line, load_args)
        """
        template_message = f"""
    Line of Code: {line_of_code}
    {Text_in_string}
    """
        template_close_message = f"""
    --------------------------------------------
    """
        programer_output.value = programer_output.value + template_message + str(variable) + template_close_message
    
    programer_output.value = programer_output.value + 'Version: 1'

