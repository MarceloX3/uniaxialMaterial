# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-06-04
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI02_A02_fileText.py
COMENTARIOS:    Genera archivo .txt asociado a cada material. 
"""

# %% [00] INTRODUCTION
# GUI en Jupyter Notebook ejecuta esta funcion para guardar diccionario con 
# toda la informacion de graficas en un archivo (.txt). Posteriormente se 
# desarrollan las graficas e impresion de codigo en base a esta informacion.


# %% [01] LIBRARIES
import json
import re
import numpy as np
import openseespy.opensees as ops
import S01_GUI02_A06_UserDefinedFunctions as udf


# %% [02] FUNCTIONS

# %%% [02-01] SUPPORT FUNCTIONS
# Function to stop the script, call as f()
def f():
    raise Exception("Found exit()")


# Function to print the variable info
def print_variable_info(var_name, var_value):
    """
    Prints the value and type of variable.
    
    Parameters:
    var_name (str): The name of the variable.
    var_value (any): The value of the variable.
    """
    print(f"{var_name} = {var_value}\nType of {var_name} = {type(var_value)}\n")


# %%% [02-02] READ (.TXT) FILES AS DICTIONARIES

def read_file_to_dict(file_path):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Replace texts in key "code" to avoid problems when reading JSON.
    replacements = {
        "'ConcreteCM'": '$ConcreteCM$',
        "'-GapClose'": "$-GapClose$",
        "'Concrete07'": "$Concrete07$",
        "'Saatcioglu(1992)'": "$Saatcioglu(1992)$",
        "'Mander(1988)'": "$Mander(1988)$",
        "'SteelMPF'": "$SteelMPF$",
        "'MinMax'": "$MinMax$",
        "'-min'": "$-min$",
        "'-max'": "$-max$",
        "'Belarbi(1994)'": "$Belarbi(1994)$",
        "'Steel02'": "$Steel02$",
        "'Steel01'": "$Steel01$",
    }
    for key, value in replacements.items():
        file_content = file_content.replace(key, value)

    # Replace single quotation marks with double quotation marks
    file_content = file_content.replace("'", '"')

    # Replace 'array(' with '[' and remove parts of the array call
    file_content = re.sub(r'array\(\[', '[', file_content)
    file_content = re.sub(r'\]\)', ']', file_content)

    # Make sure that numeric values like 'NaN' and 'inf' are valid in JSON
    file_content = file_content.replace('nan', 'null')
    file_content = file_content.replace('NaN', 'null')
    file_content = file_content.replace('inf', 'Infinity')
    file_content = file_content.replace('-inf', '-Infinity')

    # Converts the file contents to a Python dictionary
    data_dict = json.loads(file_content)

    # Convert nested lists back to numpy arrays
    if 'DataPlot' in data_dict:
        data_dict['DataPlot'] = np.array(data_dict['DataPlot'])

    # Replace dollar signs with single quotation marks
    if 'code' in data_dict:
        data_dict['code'] = data_dict['code'].replace('$', "'")

    # Delete "-" from name of model
    if 'model' in data_dict:
        data_dict['model'] = data_dict['model'].replace('-', "")

    return data_dict


# %%% [02-03] CREATE (.TXT)
def file_txt(url_arg_x, unit_x, model_args_x, load_args_x, ID_cyclic_strain, min_max_args_x = []):
    # URL_arg: Directory where save info. of plots.
    load_type, cyclic_type = load_args_x[:2]

    # Dictionary load
    if load_type == 'monotonic':
        load_type, cyclic_type, delta_e, e_max_c, e_max_t = load_args_x
        delta_e, e_max_c, e_max_t = float(delta_e), float(e_max_c), float(e_max_t)
        load = {
            "load_type": load_type,
            "cyclic_type": cyclic_type,
            "delta_e": delta_e,
            "e_max_c": e_max_c,
            "e_max_t": e_max_t
        }

    elif load_type == 'cyclic':
        if cyclic_type == 'compression':
            load_type, cyclic_type, delta_e, e_max_c_1, pulso_1, e_max_c_2, pulso_2, e_max_c_3, pulso_3, e_max_c_4, pulso_4, e_max_c_5, pulso_5 = load_args_x
            delta_e, e_max_c_1, pulso_1, e_max_c_2, pulso_2, e_max_c_3, pulso_3, e_max_c_4, pulso_4, e_max_c_5, pulso_5 = float(
                delta_e), float(e_max_c_1), int(pulso_1), float(e_max_c_2), int(pulso_2), float(e_max_c_3), int(pulso_3), float(
                    e_max_c_4), int(pulso_4), float(e_max_c_5), int(pulso_5)
            load = {
                "load_type": load_type,
                "cyclic_type": cyclic_type,
                "delta_e": delta_e,
                "e_max_c": [e_max_c_1, e_max_c_2, e_max_c_3, e_max_c_4, e_max_c_5],
                "pulso_c": [pulso_1, pulso_2, pulso_3, pulso_4, pulso_5]
            }
        elif cyclic_type == 'traction':
            load_type, cyclic_type, delta_e, e_max_t_1, pulso_1, e_max_t_2, pulso_2, e_max_t_3, pulso_3, e_max_t_4, pulso_4, e_max_t_5, pulso_5 = load_args_x
            delta_e, e_max_t_1, pulso_1, e_max_t_2, pulso_2, e_max_t_3, pulso_3, e_max_t_4, pulso_4, e_max_t_5, pulso_5 = float(
                delta_e), float(e_max_t_1), int(pulso_1), float(e_max_t_2), int(pulso_2), float(e_max_t_3), int(pulso_3), float(
                    e_max_t_4), int(pulso_4), float(e_max_t_5), int(pulso_5)
            load = {
                "load_type": load_type,
                "cyclic_type": cyclic_type,
                "delta_e": delta_e,
                "e_max_t": [e_max_t_1, e_max_t_2, e_max_t_3, e_max_t_4, e_max_t_5],
                "pulso_t": [pulso_1, pulso_2, pulso_3, pulso_4, pulso_5]
            }
        elif cyclic_type == 'combined':
            load_type, cyclic_type, delta_e, e_max_c_1, e_max_t_1, pulso_1, e_max_c_2, e_max_t_2, pulso_2, e_max_c_3, e_max_t_3, pulso_3, e_max_c_4, e_max_t_4, pulso_4, e_max_c_5, e_max_t_5, pulso_5 = load_args_x
            delta_e, e_max_c_1, e_max_t_1, pulso_1, e_max_c_2, e_max_t_2, pulso_2, e_max_c_3, e_max_t_3, pulso_3, e_max_c_4, e_max_t_4, pulso_4, e_max_c_5, e_max_t_5, pulso_5 = float(
                delta_e), float(e_max_c_1), float(e_max_t_1), int(pulso_1), float(e_max_c_2), float(e_max_t_2), int(pulso_2), float(e_max_c_3), float(e_max_t_3), int(pulso_3), float(
                    e_max_c_4), float(e_max_t_4), int(pulso_4), float(e_max_c_5), float(e_max_t_5), int(pulso_5)
            load = {
                "load_type": load_type,
                "cyclic_type": cyclic_type,
                "delta_e": delta_e,
                "e_max_c": [e_max_c_1, e_max_c_2, e_max_c_3, e_max_c_4, e_max_c_5],
                "e_max_t": [e_max_t_1, e_max_t_2, e_max_t_3, e_max_t_4, e_max_t_5],
                "pulso": [pulso_1, pulso_2, pulso_3, pulso_4, pulso_5]
            }
    
    model = model_args_x[0]

    # Dictionary material
    if model == 'ConcreteCM':
        model, mat_tag, fpcc, epcc, Ec, rc, xcrn, ft, et, rt, xcrp, GapClose = model_args_x
        mat_tag, fpcc, epcc, Ec, rc, xcrn, ft, et, rt, xcrp, GapClose = int(mat_tag), float(fpcc), float(epcc), float(
            Ec), float(rc), float(xcrn), float(ft), float(et), float(rt), float(xcrp), int(GapClose)
        
        # If there is a MinMax material, it's necessary change the mat_tag
        if len(min_max_args_x) != 0:
            OtherTag_minmax = min_max_args_x[2]
            OtherTag_minmax = int(OtherTag_minmax)
            mat_tag = OtherTag_minmax
        
        material = {
            "model": "-ConcreteCM",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "fpcc": fpcc,
                "epcc": epcc,
                "Ec": Ec,
                "rc": rc,
                "xcrn": xcrn,
                "ft": ft,
                "et": et,
                "rt": rt,
                "xcrp": xcrp,
                "GapClose": GapClose
            },
            "code": f"""# import openseespy.opensees as ops

# {unit_x} =  #  complete this field.
            
matTag_{mat_tag}   = {mat_tag}
fpcc_{mat_tag}     = {fpcc} #  * {unit_x}
epcc_{mat_tag}     = {epcc}
ft_{mat_tag}       = {ft} #  * {unit_x}
et_{mat_tag}       = {et}
Ecc_{mat_tag}      = {Ec} #  * {unit_x}
xcrnc_{mat_tag}    = {xcrn}
xcrp_{mat_tag}     = {xcrp}
rc_{mat_tag}       = {rc}
rt_{mat_tag}       = {rt}
GapClose_{mat_tag} = {GapClose}

ops.uniaxialMaterial('ConcreteCM', matTag_{mat_tag}, fpcc_{mat_tag}, epcc_{mat_tag}, Ecc_{mat_tag}, rc_{mat_tag}, xcrnc_{mat_tag}, ft_{mat_tag}, et_{mat_tag}, rt_{mat_tag}, xcrp_{mat_tag}, '-GapClose', GapClose_{mat_tag})
"""
        }

    elif model == 'Concrete07':
        model, mat_tag, fc, epsc, Ec, ft, et, xp, xn, r = model_args_x
        mat_tag, fc, epsc, Ec, ft, et, xp, xn, r = int(mat_tag), float(fc), float(epsc), float(Ec), float(ft), float(
            et), float(xp), float(xn), float(r)
        
        # If there is a MinMax material, it's necessary change the mat_tag
        if len(min_max_args_x) != 0:
            OtherTag_minmax = min_max_args_x[2]
            OtherTag_minmax = int(OtherTag_minmax)
            mat_tag = OtherTag_minmax
        
        material = {
            "model": "-Concrete07",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "fc": fc,
                "epsc": epsc,
                "Ec": Ec,
                "ft": ft,
                "et": et,
                "xp": xp,
                "xn": xn,
                "r": r
            },
            "code": f"""# import openseespy.opensees as ops

# {unit_x} =  #  complete this field.

matTag_{mat_tag} = {mat_tag}
fc_{mat_tag}     = {fc} #  * {unit_x}
epsc_{mat_tag}   = {epsc}
Ec_{mat_tag}     = {Ec} #  * {unit_x}
ft_{mat_tag}     = {ft} #  * {unit_x}
et_{mat_tag}     = {et}
xp_{mat_tag}     = {xp}
xn_{mat_tag}     = {xn}
r_{mat_tag}      = {r}

ops.uniaxialMaterial('Concrete07', matTag_{mat_tag}, fc_{mat_tag}, epsc_{mat_tag}, Ec_{mat_tag}, ft_{mat_tag}, et_{mat_tag}, xp_{mat_tag}, xn_{mat_tag}, r_{mat_tag})
"""
        }

    elif model == 'SteelMPF':
        model, mat_tag, fyp, fyn, E0, bp, bn, R0, cR1, cR2, a1, a2, a3, a4 = model_args_x
        mat_tag, fyp, fyn, E0, bp, bn, R0, cR1, cR2, a1, a2, a3, a4 = int(mat_tag), float(fyp), float(fyn), float(
            E0), float(bp), float(bn), float(R0), float(cR1), float(cR2), float(a1), float(a2), float(a3), float(a4)
        
        # If there is a MinMax material, it's necessary change the mat_tag
        if len(min_max_args_x) != 0:
            OtherTag_minmax = min_max_args_x[2]
            OtherTag_minmax = int(OtherTag_minmax)
            mat_tag = OtherTag_minmax
        
        material = {
            "model": "-SteelMPF",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "fyp": fyp,
                "fyn": fyn,
                "E0": E0,
                "bp": bp,
                "bn": bn,
                "R0": R0,
                "cR1": cR1,
                "cR2": cR2,
                "a1": a1,
                "a2": a2,
                "a3": a3,
                "a4": a4
            },
            "code": f"""# import openseespy.opensees as ops

# {unit_x} =  #  complete this field.

matTag_{mat_tag} = {mat_tag}
fyp_{mat_tag}    = {fyp} #  * {unit_x}
fyn_{mat_tag}    = {fyn} #  * {unit_x}
E0_{mat_tag}     = {E0} #  * {unit_x}
bp_{mat_tag}     = {bp}
bn_{mat_tag}     = {bn}
R0_{mat_tag}     = {R0}
cR1_{mat_tag}    = {cR1}
cR2_{mat_tag}    = {cR2}
a1_{mat_tag}     = {a1}
a2_{mat_tag}     = {a2}
a3_{mat_tag}     = {a3}
a4_{mat_tag}     = {a4}

ops.uniaxialMaterial('SteelMPF', matTag_{mat_tag}, fyp_{mat_tag}, fyn_{mat_tag}, E0_{mat_tag}, bp_{mat_tag}, bn_{mat_tag}, R0_{mat_tag}, cR1_{mat_tag}, cR2_{mat_tag}, a1_{mat_tag}, a2_{mat_tag}, a3_{mat_tag}, a4_{mat_tag})
"""
        }
    
    elif model == 'Steel02':
        model, mat_tag, Fy, E0, b, R0, cR1, cR2, a1, a2, a3, a4, sigInit = model_args_x
        mat_tag, Fy, E0, b, R0, cR1, cR2, a1, a2, a3, a4, sigInitg = int(
            mat_tag), float(Fy), float(E0), float(b), float(R0), 
        float(cR1), float(cR2), float(a1), float(a2), float(a3), float(a4),
        float(sigInit)
        
        # If there is a MinMax material, it's necessary change the mat_tag
        if len(min_max_args_x) != 0:
            OtherTag_minmax = min_max_args_x[2]
            OtherTag_minmax = int(OtherTag_minmax)
            mat_tag = OtherTag_minmax
        
        material = {
            "model": "-Steel02",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "Fy": Fy,
                "E0": E0,
                "b": b,
                "R0": R0,
                "cR1": cR1,
                "cR2": cR2,
                "a1": a1,
                "a2": a2,
                "a3": a3,
                "a4": a4,
                "sigInit": sigInit
            },
            "code": f"""# import openseespy.opensees as ops
# {unit_x} =  #  complete this field.

matTag_{mat_tag} = {mat_tag}
Fy_{mat_tag}     = {Fy} #  * {unit_x}
E0_{mat_tag}     = {E0} #  * {unit_x}
b_{mat_tag}      = {b}
R0_{mat_tag}     = {R0}
cR1_{mat_tag}    = {cR1}
cR2_{mat_tag}    = {cR2}
a1_{mat_tag}     = {a1}
a2_{mat_tag}     = {a2}
a3_{mat_tag}     = {a3}
a4_{mat_tag}     = {a4}
sigInit_{mat_tag} = {sigInit}

ops.uniaxialMaterial('Steel02', matTag_{mat_tag}, Fy_{mat_tag}, E0_{mat_tag}, b_{mat_tag}, R0_{mat_tag}, cR1_{mat_tag}, cR2_{mat_tag}, a1_{mat_tag}, a2_{mat_tag}, a3_{mat_tag}, a4_{mat_tag}, sigInit_{mat_tag})
"""
        }
    
    elif model == 'Steel01':
        model, mat_tag, Fy, E0, b, a1, a2, a3, a4 = model_args_x
        mat_tag, Fy, E0, b, a1, a2, a3, a4 = int(
            mat_tag), float(Fy), float(E0), float(b), float(a1), float(a2), float(a3), float(a4)
        
        # If there is a MinMax material, it's necessary change the mat_tag
        if len(min_max_args_x) != 0:
            OtherTag_minmax = min_max_args_x[2]
            OtherTag_minmax = int(OtherTag_minmax)
            mat_tag = OtherTag_minmax
        
        material = {
            "model": "-Steel01",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "Fy": Fy,
                "E0": E0,
                "b": b,
                "a1": a1,
                "a2": a2,
                "a3": a3,
                "a4": a4
            },
            "code": f"""# import openseespy.opensees as ops
# {unit_x} =  #  complete this field.

matTag_{mat_tag} = {mat_tag}
Fy_{mat_tag}     = {Fy} #  * {unit_x}
E0_{mat_tag}     = {E0} #  * {unit_x}
b_{mat_tag}      = {b}
a1_{mat_tag}     = {a1}
a2_{mat_tag}     = {a2}
a3_{mat_tag}     = {a3}
a4_{mat_tag}     = {a4}

ops.uniaxialMaterial('Steel01', matTag_{mat_tag}, Fy_{mat_tag}, E0_{mat_tag}, b_{mat_tag}, a1_{mat_tag}, a2_{mat_tag}, a3_{mat_tag}, a4_{mat_tag})
"""
        }

    elif model == 'Saatcioglu(1992)':
        model, mat_tag, fco, fl, e01, rho, e085 = model_args_x
        mat_tag, fco, fl, e01, rho, e085 = int(mat_tag), float(fco), float(fl), float(e01), float(rho), float(e085)
        # Unified unit for requirements in User Defined Functions
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
        # Units conversion
        fco = fco * unit_factors_new['MPa'][unit_x]
        fl = fl * unit_factors_new['MPa'][unit_x]
        # Others values:
        k1 = 6.7 * (fl) ** (-0.17)  # where k1 is calculated using Eq (5) or (9)
        fcc = fco + k1 * fl  # where fcc is calculated using Eq (4) or (6)
        K = (k1 * fl) / fco  # where K is calculated using Eq (13)
        e1 = e01 * (1 + 5 * K)  # where e1 is calculated using Eq (12)
        e85 = 260 * rho * e1 + e085  # where e85 is calculated using Eq (14)
        # After calculations of parameters return to the original system of units.
        fco = fco * unit_factors_new[unit_x]['MPa']
        fl = fl * unit_factors_new[unit_x]['MPa']
        
        # Dictionary
        material = {
            "model": "Saatcioglu(1992)",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "fco": fco,
                "fl": fl,
                "e01": e01,
                "rho": rho,
                "e085": e085
            },
            "code": f"""Inputs 'Saatcioglu(1992)':

matTag_{mat_tag} = {mat_tag}
fco_{mat_tag}    = {fco} #  * MPa
fle_{mat_tag}    = {fl} #  * MPa
e01_{mat_tag}    = {e01}
rho_{mat_tag}    = {rho}
e085_{mat_tag}   = {e085}

Others parameters of the model:
k1_{mat_tag}     = {round(k1, 4)}  # where k1 is calculated using Eq (5) or (9)
fcc_{mat_tag}    = {round(fcc, 4)}  #  * MPa where fcc is calculated using Eq (4) or (6)
K_{mat_tag}      = {round(K, 4)}  # where K is calculated using Eq (13)
e1_{mat_tag}     = {round(e1, 4)}  # where e1 is calculated using Eq (12)
e85_{mat_tag}    = {round(e85, 4)}  # where e85 is calculated using Eq (14)
"""
        }

    elif model == 'Mander(1988)':
        model, mat_tag, fco, CSR, eco, Ec = model_args_x
        mat_tag, fco, CSR, eco, Ec = int(mat_tag), float(fco), float(CSR), float(eco), float(Ec)

        fcc = CSR * fco  # 1. Calculate fcc using CSR
        ecc = eco * (1 + 5 * (CSR - 1))  # 2. Calculate ecc using Eq (5)
        Esec = fcc / ecc  # 3. Calculate Esec using Eq (8)
        r = Ec / (Ec - Esec)  # 4. Calculate r using Eq (6)

        # Dictionary
        material = {
            "model": "Mander(1988)",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "fco": fco,
                "CSR": CSR,
                "eco": eco,
                "Ec": Ec
            },
            "code": f"""Inputs 'Mander(1988)':

matTag_{mat_tag} = {mat_tag}
fco_{mat_tag}    = {fco} #  * {unit_x}
CSR_{mat_tag}    = {CSR}
eco_{mat_tag}    = {eco}
Ec_{mat_tag}     = {Ec} #  * {unit_x}

Others parameters of the model:
fcc_{mat_tag}    = {round(fcc, 4)}  # 1. Calculate fcc using CSR
ecc_{mat_tag}    = {round(ecc, 4)}  # 2. Calculate ecc using Eq (5)
Esec_{mat_tag}   = {round(Esec, 4)}  # 3. Calculate Esec using Eq (8)
r_{mat_tag}      = {round(r, 4)}  # 4. Calculate r using Eq (6)
"""
        }
        
    elif model == 'Belarbi(1994)':
        model, mat_tag, fcr, eps_cr, Ecr = model_args_x
        mat_tag, fcr, eps_cr, Ecr = int(mat_tag), float(fcr), float(eps_cr), float(Ecr)

        # Dictionary
        material = {
            "model": "Belarbi(1994)",
            "unit": unit_x,
            "material": {
                "matTag": mat_tag,
                "fcr": fcr,
                "eps_cr": eps_cr,
                "Ecr": Ecr
            },
            "code": f"""Inputs 'Belarbi(1994)':

matTag_{mat_tag} = {mat_tag}
fcr_{mat_tag}    = {fcr} #  * {unit_x}
eps_cr_{mat_tag} = {eps_cr}
Ecr_{mat_tag}    = {Ecr} #  * {unit_x}
"""
        }
    
    # If there is a MinMax material, add and modify the information in the dictionary
    if len(min_max_args_x) != 0:
        mat_type_minmax, matTag_minmax, OtherTag_minmax, minStrain, maxStrain = min_max_args_x
        matTag_minmax, OtherTag_minmax, minStrain, maxStrain = int(matTag_minmax), int(OtherTag_minmax), float(minStrain), float(maxStrain)
        
        # Add new key "material_min_max" to the dictionary
        material["material_min_max"] = {
            "matTag_minmax": mat_type_minmax,
            "OtherTag_minmax": OtherTag_minmax,
            "minStrain": minStrain,
            "maxStrain": maxStrain
            }
        
        # Modify the "code" key to add the information of the MinMax material
        material["code"] += f"""
# MinMax material
matTag_minmax_{matTag_minmax}   = {matTag_minmax}
OtherTag_minmax_{matTag_minmax} = {OtherTag_minmax}
minStrain_{matTag_minmax}       = {minStrain}
maxStrain_{matTag_minmax}       = {maxStrain}

ops.uniaxialMaterial('MinMax', matTag_minmax_{matTag_minmax}, OtherTag_minmax_{matTag_minmax}, '-min', minStrain_{matTag_minmax}, '-max', maxStrain_{matTag_minmax})
"""
        # Create file (aux.txt) with data of plot (necessary for extension of data)
        dictionary = data_plot(unit_x, model_args_x, load_args_x, min_max_args_x = min_max_args_x)
    
    else:
        # Create file (aux.txt) with data of plot (necessary for extension of data)
        dictionary = data_plot(unit_x, model_args_x, load_args_x) 
    
    # Joint dictionaries
    # file URL with the dictionary
    URL = "aux_file.txt"
    # Reads the contents of the file
    plot = read_file_to_dict(URL)
    # Joint dictionaries 
    MatInfo = {**load, **material, **plot}
    
    # The name of the file change if this is a MinMax material
    if len(min_max_args_x) != 0:
        url_file = url_arg_x + f"MatTag_{OtherTag_minmax}_{matTag_minmax}_IdStrainLoad_{ID_cyclic_strain}.txt"
    else:
        url_file = url_arg_x + f"MatTag_{mat_tag}_IdStrainLoad_{ID_cyclic_strain}.txt"
    # Convert numpy arrays to lists for write file .txt
    MatInfo['DataPlot'] = MatInfo['DataPlot'].tolist()
    # Write the dictionary to .txt file
    with open(url_file, 'w') as file:
        json.dump(MatInfo, file)

    return MatInfo


# %%% [02-01] CREATE DATA PLOT
# Function make strains for the analysis
def generate_strains(e_min, e_max, puntos, pulses):
    strains_c = np.linspace(e_min, e_max, puntos)
    strains_d = np.linspace(e_max, e_min, puntos)
    single_peak = np.concatenate((strains_c, strains_d))
    if pulses != 0:
        strains = np.concatenate([single_peak] * pulses)
    else:
        return []
    return strains


# Function make strains for the analysis
def generate_strains_2(e_min, e_max, delta_e, pulses):
    pts_1 = int(abs(e_min) / delta_e)
    strains_1 = np.linspace(0, e_min, pts_1)
    pts_2 = int((abs(e_min) + abs(e_max)) / delta_e)
    strains_2 = np.linspace(e_min, e_max, pts_2)
    pts_3 = int(abs(e_max) / delta_e)
    strains_3 = np.linspace(e_max, 0, pts_3)
    single_peak = np.concatenate((strains_1, strains_2, strains_3))
    if pulses != 0:
        strains = np.concatenate([single_peak] * pulses)
    else:
        return []
    return strains


# Function remove consecutive duplicates values
def remove_consecutive_duplicates(array):
    new_array = [array[0]]
    for i in range(1, len(array)):
        if array[i] != array[i - 1]:
            new_array.append(array[i])
    return np.array(new_array)

# Function to calculate the strains for the load monotonic and cyclic
def strain_load(load_args_x):
    load_type, cyclic_type = load_args_x[:2]
    if load_type == 'monotonic':
        load_type, cyclic_type, delta_e, e_max_c, e_max_t = load_args_x
        delta_e, e_max_c, e_max_t = float(delta_e), float(e_max_c), float(e_max_t)
        
        # Calculate the number of points for compression and tension
        pts_c = int(abs(e_max_c) / delta_e)
        pts_t = int(abs(e_max_t) / delta_e)
        
        # Generate strains for compression and tension
        strains_C = np.linspace(0, e_max_c, pts_c)
        strains_T = np.linspace(0, e_max_t, pts_t)
        strains_C, strains_T = strains_C.tolist(), strains_T.tolist()
        return strains_C, strains_T
    
    elif load_type == 'cyclic':
        if cyclic_type == 'compression':
            load_type, cyclic_type, delta_e, e_max_c_1, pulso_1, e_max_c_2, pulso_2, e_max_c_3, pulso_3, e_max_c_4, pulso_4, e_max_c_5, pulso_5 = load_args_x
            delta_e, e_max_c_1, pulso_1, e_max_c_2, pulso_2, e_max_c_3, pulso_3, e_max_c_4, pulso_4, e_max_c_5, pulso_5 = float(
                delta_e), float(e_max_c_1), int(pulso_1), float(e_max_c_2), int(pulso_2), float(e_max_c_3), int(pulso_3), float(
                    e_max_c_4), int(pulso_4), float(e_max_c_5), int(pulso_5)

            # Calculate the number of points for each peak
            pts_c_1 = int(abs(e_max_c_1) / delta_e)
            pts_c_2 = int(abs(e_max_c_2) / delta_e)
            pts_c_3 = int(abs(e_max_c_3) / delta_e)
            pts_c_4 = int(abs(e_max_c_4) / delta_e)
            pts_c_5 = int(abs(e_max_c_5) / delta_e)
            
            # Generate strains for each peak and concatenate them
            strains_C_1 = generate_strains(0, e_max_c_1, pts_c_1, pulso_1)
            strains_C_2 = generate_strains(0, e_max_c_2, pts_c_2, pulso_2)
            strains_C_3 = generate_strains(0, e_max_c_3, pts_c_3, pulso_3)
            strains_C_4 = generate_strains(0, e_max_c_4, pts_c_4, pulso_4)
            strains_C_5 = generate_strains(0, e_max_c_5, pts_c_5, pulso_5)
            strains_C = np.concatenate((strains_C_1, strains_C_2, strains_C_3, strains_C_4, strains_C_5))

            # Remove consecutive duplicates values
            strains_C = remove_consecutive_duplicates(strains_C)
            return strains_C
        
        elif cyclic_type == 'traction':
            load_type, cyclic_type, delta_e, e_max_t_1, pulso_1, e_max_t_2, pulso_2, e_max_t_3, pulso_3, e_max_t_4, pulso_4, e_max_t_5, pulso_5 = load_args_x
            delta_e, e_max_t_1, pulso_1, e_max_t_2, pulso_2, e_max_t_3, pulso_3, e_max_t_4, pulso_4, e_max_t_5, pulso_5 = float(
                delta_e), float(e_max_t_1), int(pulso_1), float(e_max_t_2), int(pulso_2), float(e_max_t_3), int(pulso_3), float(
                    e_max_t_4), int(pulso_4), float(e_max_t_5), int(pulso_5)
            
            # Calculate the number of points for each peak
            pts_t_1 = int(abs(e_max_t_1) / delta_e)
            pts_t_2 = int(abs(e_max_t_2) / delta_e)
            pts_t_3 = int(abs(e_max_t_3) / delta_e)
            pts_t_4 = int(abs(e_max_t_4) / delta_e)
            pts_t_5 = int(abs(e_max_t_5) / delta_e)

            # Generate strains for each peak and concatenate them
            strains_T_1 = generate_strains(0, e_max_t_1, pts_t_1, pulso_1)
            strains_T_2 = generate_strains(0, e_max_t_2, pts_t_2, pulso_2)
            strains_T_3 = generate_strains(0, e_max_t_3, pts_t_3, pulso_3)
            strains_T_4 = generate_strains(0, e_max_t_4, pts_t_4, pulso_4)
            strains_T_5 = generate_strains(0, e_max_t_5, pts_t_5, pulso_5)
            strains_T = np.concatenate((strains_T_1, strains_T_2, strains_T_3, strains_T_4, strains_T_5))

            # Remove consecutive duplicates values
            strains_T = remove_consecutive_duplicates(strains_T)
            return strains_T
        
        elif cyclic_type == 'combined':
            load_type, cyclic_type, delta_e, e_max_c_1, e_max_t_1, pulso_1, e_max_c_2, e_max_t_2, pulso_2, e_max_c_3, e_max_t_3, pulso_3, e_max_c_4, e_max_t_4, pulso_4, e_max_c_5, e_max_t_5, pulso_5 = load_args_x
            delta_e, e_max_c_1, e_max_t_1, pulso_1, e_max_c_2, e_max_t_2, pulso_2, e_max_c_3, e_max_t_3, pulso_3, e_max_c_4, e_max_t_4, pulso_4, e_max_c_5, e_max_t_5, pulso_5 = float(
                delta_e), float(e_max_c_1), float(e_max_t_1), int(pulso_1), float(e_max_c_2), float(e_max_t_2), int(pulso_2), float(e_max_c_3), float(e_max_t_3), int(pulso_3), float(
                    e_max_c_4), float(e_max_t_4), int(pulso_4), float(e_max_c_5), float(e_max_t_5), int(pulso_5)

            # Generate strains for each peak and concatenate them
            strains_D_1 = generate_strains_2(e_max_c_1, e_max_t_1, delta_e, pulso_1)
            strains_D_2 = generate_strains_2(e_max_c_2, e_max_t_2, delta_e, pulso_2)
            strains_D_3 = generate_strains_2(e_max_c_3, e_max_t_3, delta_e, pulso_3)
            strains_D_4 = generate_strains_2(e_max_c_4, e_max_t_4, delta_e, pulso_4)
            strains_D_5 = generate_strains_2(e_max_c_5, e_max_t_5, delta_e, pulso_5)
            strains_D = np.concatenate((strains_D_1, strains_D_2, strains_D_3, strains_D_4, strains_D_5))

            # Remove consecutive duplicates values
            strains_D = remove_consecutive_duplicates(strains_D)
            return strains_D
        
        
# Calculate stress for graphic
def data_plot(unit_x, model_args_x, load_args_x, min_max_args_x = []):
    # Extract the arguments
    load_type, cyclic_type = load_args_x[:2]
    # Identify opensees models already implemented in the script
    models_opss_py = ['ConcreteCM', 'Concrete07', 'SteelMPF', 'Steel02', 'Steel01']

    if load_type == 'monotonic':
        
        # Calculate strains for the monotonic load
        strains_C, strains_T = strain_load(load_args_x)
        stresses_C, stresses_T = [], []

        model = model_args_x[0]
        
        # If model is defined in openseespy.
        if model in models_opss_py:
            # Define test.
            exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A04_2_testUniaxialMaterial.py', encoding='utf8').read())
            for i in range(len(strains_C)):
                # Calculate strength
                ops.setStrain(strains_C[i])
                stresses_C.append(ops.getStress())
        else:
            # Calculate stresses for compression
            for i in range(len(strains_C)):
                # If model is defined by user.
                if model == 'Saatcioglu(1992)':
                    ec = strains_C[i]
                    # Calculate strength
                    fc = udf.Saatcioglu_1992(unit_x, abs(ec), model_args_x[2:])
                    stresses_C.append(-fc)
                elif model == 'Mander(1988)':
                    ec = strains_C[i]
                    # Calculate strength
                    fc = udf.Mander_1988(unit_x, abs(ec), model_args_x[2:])
                    stresses_C.append(-fc)

        # Calculate stresses for tension
        # If model is defined in openseespy.
        if model in models_opss_py:
            # Define test.
            exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A04_2_testUniaxialMaterial.py', encoding='utf8').read())
            for i in range(len(strains_T)):
                # Calculate strength
                ops.setStrain(strains_T[i])
                stresses_T.append(ops.getStress())
        else:
            for i in range(len(strains_T)):
                # If model is defined by user.
                if model == 'Belarbi(1994)':
                    ec = strains_T[i]
                    # Calculate strength
                    ft = udf.Belarbi_1994(unit_x, abs(ec), model_args_x[2:])
                    stresses_T.append(ft)

        # Convert the results to numpy arrays
        strains_C, stresses_C = np.array(strains_C), np.array(stresses_C)
        strains_T, stresses_T = np.array(strains_T), np.array(stresses_T)

        # Ensure both arrays are the same length by padding with NaNs
        max_length = max(len(strains_C), len(strains_T))

        def pad_with_nan(array, target_length):
            padding_length = target_length - len(array)
            return np.pad(array, (0, padding_length), constant_values=np.nan)

        strains_C = pad_with_nan(strains_C, max_length)
        stresses_C = pad_with_nan(stresses_C, max_length)
        strains_T = pad_with_nan(strains_T, max_length)
        stresses_T = pad_with_nan(stresses_T, max_length)

        # Combine the data into columns
        data = np.column_stack((strains_C, stresses_C, strains_T, stresses_T))
        # Create a dictionary to store the data
        dictionary = {"DataPlot": data}

    elif load_type == 'cyclic':
        if cyclic_type == 'compression':
            # Calculate strains for the cyclic load
            strains_C = strain_load(load_args_x)

            # Calculate stresses for the cyclic load
            stresses_C = []
            for i in range(len(strains_C)):
                model = model_args_x[0]
                # If model is defined in openseespy.
                if model in models_opss_py:
                    # Define test.
                    exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A04_2_testUniaxialMaterial.py', encoding='utf8').read())
                    # Calculate strength
                    if i == 0:
                        ops.setStrain(strains_C[i])
                    else:
                        for k in range(i + 1):
                            ops.setStrain(strains_C[k])
                    stresses_C.append(ops.getStress())
                # If model is defined by user.
                elif model == 'Saatcioglu(1992)':
                    fc = 0  # Saatcioglu only define model under monotonic load.
                    stresses_C.append(fc)
                elif model == 'Mander(1988)':
                    fc = 0
                    stresses_C.append(fc)
                elif model == 'Belarbi(1994)':
                    fc = 0
                    stresses_C.append(fc)

            # Convert the results to numpy arrays
            strains_C, stresses_C = np.array(strains_C), np.array(stresses_C)
            # Combine the data into columns
            data = np.column_stack((strains_C, stresses_C))
            # Create a dictionary to store the data
            dictionary = {"DataPlot": data}

        elif cyclic_type == 'traction':
            # Calculate strain for the cyclic load
            strains_T = strain_load(load_args_x)

            # Calculate stresses for the cyclic load
            stresses_T = []
            for i in range(len(strains_T)):
                model = model_args_x[0]
                # If model is defined in openseespy.
                if model in models_opss_py:
                    exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A04_2_testUniaxialMaterial.py', encoding='utf8').read())
                    # Calculate strength
                    if i == 0:
                        ops.setStrain(strains_T[i])
                    else:
                        for k in range(i + 1):
                            ops.setStrain(strains_T[k])
                    stresses_T.append(ops.getStress())
                # If model is defined by user.
                elif model == 'Saatcioglu(1992)':
                    fc = 0
                    stresses_T.append(fc)
                elif model == 'Mander(1988)':
                    fc = 0
                    stresses_T.append(fc)
                elif model == 'Belarbi(1994)':
                    fc = 0
                    stresses_T.append(fc)

            # Convert the results to numpy arrays
            strains_T, stresses_T = np.array(strains_T), np.array(stresses_T)
            # Combine the data into columns
            data = np.column_stack((strains_T, stresses_T))
            # Create a dictionary to store the data
            dictionary = {"DataPlot": data}

        elif cyclic_type == 'combined':
            # Calculate strains for the cyclic load
            strains_D = strain_load(load_args_x)

            # Calculate stresses for the cyclic load
            stresses_D = []
            for i in range(len(strains_D)):
                model = model_args_x[0]
                # If model is defined in openseespy.
                if model in models_opss_py:
                    # Define test.
                    exec(open('C_GUI02_uniaxialMaterial/S01_GUI02_A04_2_testUniaxialMaterial.py', encoding='utf8').read())
                    # Calculate strength
                    if i == 0:
                        ops.setStrain(strains_D[i])
                    else:
                        for k in range(i + 1):
                            ops.setStrain(strains_D[k])
                    stresses_D.append(ops.getStress())
                # If model is defined by user.
                elif model == 'Saatcioglu(1992)':
                    fc = 0
                    stresses_D.append(fc)
                elif model == 'Mander(1988)':
                    fc = 0
                    stresses_D.append(fc)
                elif model == 'Belarbi(1994)':
                    fc = 0
                    stresses_D.append(fc)

            # Convert the results to numpy arrays
            strains_D, stresses_D = np.array(strains_D), np.array(stresses_D)
            # Combine the data into columns
            data = np.column_stack((strains_D, stresses_D))
            # Create a dictionary to store the data
            dictionary = {"DataPlot": data}

    # Convert numpy arrays to lists
    dictionary['DataPlot'] = dictionary['DataPlot'].tolist()

    # Write the dictionary to a .txt file
    with open('aux_file.txt', 'w') as file:
        json.dump(dictionary, file)
        
    
    # For fast running, I'm going to return directly the dictionary with the data of the plot.
    # And I'm going to include some necessary data for the plot.
    # Add key unit in the dictionary
    dictionary['unit'] = unit_x
    # Add key model in the dictionary
    dictionary['model'] = model_args_x[0]
    # Add key load_type in the dictionary
    dictionary['load_type'] = load_args_x[0]
    # Add key cyclic_type in the dictionary
    dictionary['cyclic_type'] = load_args_x[1]
    # Add key material in the dictionary
    if len(min_max_args_x) != 0:
        dictionary['material'] = {'matTag': min_max_args_x[1]}  # min_max_args[1]
    else:
        dictionary['material'] = {'matTag': model_args_x[1]}  # model_args_x[1]
    
    return dictionary


# %% [03] TEST FUNCTIONS

# %%% [03-00] file_txt()
if __name__ == '__main__':
    # Example 1:
    run_example_1 = False
    if run_example_1:
        unit = 'kgf/cm**2'
        model_args = ['ConcreteCM', 3, '-287.0', '-0.0035', '255810.222626071', '3.5', '1.05', '34.78', '0.0001', '7', '10000', '1']
        load_args = ['monotonic', '-', '0.0001', '-0.008', '0']
        min_max_args = ['MinMax', 3, '2', '-6.0e-3', '1.0e16']
        # min_max_args = ['MinMax', 3, '2', '-1.0e16', '1.0e16']
        
        dictionary = data_plot(unit, model_args, load_args, min_max_args_x = min_max_args)
        # print(dictionary)
        
    # Example 2:
    run_example_2 = False
    if run_example_2:
        unit = 'kgf/cm**2'
        model_args = ['ConcreteCM', 1, '-250.0', '-0.002', '238751.9633', '7', '1.05', '34.78', '0.0001', '7', '10000', '1']
        load_args = ['monotonic', '-', '0.0001', '-0.008', '0']
        
        dictionary = data_plot(unit, model_args, load_args)
        print(dictionary)
        
    # Example 3:
    run_example_3 = False
    if run_example_3:
        url_args = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/monotonic/'
        unit = 'kgf/cm**2'
        model_args = ['ConcreteCM', 5, '-250.0', '-0.002', '238751.9633', '7', '1.05', '34.78', '0.0001', '7', '10000', '1']
        load_args = ['monotonic', '-', '0.0001', '-0.008', '0']
        ID_cyclic_strain = 'Default'
        
        file_txt(url_args, unit, model_args, load_args, ID_cyclic_strain)
        
    # Example 4:
    run_example_4 = False
    if run_example_4:
        url_args = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/monotonic/'
        unit = 'kgf/cm**2'
        model_args = ['ConcreteCM', 5, '-250.0', '-0.002', '238751.9633', '7', '1.05', '34.78', '0.0001', '7', '10000', '1']
        load_args = ['monotonic', '-', '0.0001', '-0.008', '0']
        ID_cyclic_strain = 'Default'
        min_max_args = ['MinMax', 6, '5', '-6e-3', '1.0e16']
        
        file_txt(url_args, unit, model_args, load_args, ID_cyclic_strain, min_max_args_x = min_max_args)

    # Example 5:
    run_example_5 = False
    if run_example_5:
        url_x = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/monotonic/MatTag_4_5_IdStrainLoad_Default.txt'
        data_dict = read_file_to_dict(url_x)
        print("data_dict['load_type'] = ", data_dict['load_type'])
        
    # Example 6:
    run_example_6 = False
    if run_example_6:
        url_args = 'C_GUI02_uniaxialMaterial/C_GUI02_uniaxialMaterial/monotonic/'
        unit = 'ksi'
        model_args = ['ConcreteCM', 10, '-5.2436', '-0.00414', '4592.3', '7', '1.025', '0.255', '0.00008', '1.2', '10000', '0']
        load_args = ['monotonic', '-', '0.00025', '-0.02', '0']
        ID_cyclic_strain = '2'
        min_max_args = ['MinMax', 10, 7, '-0.01593', '1.0e16']
        file_txt(url_args, unit, model_args, load_args, ID_cyclic_strain, min_max_args_x = min_max_args)
        print("Archivo creado con éxito.")
        
        