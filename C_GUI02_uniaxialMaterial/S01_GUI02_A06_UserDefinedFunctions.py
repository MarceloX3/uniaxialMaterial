# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-06-04
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI02_A06_UserDefinedFunctions.py
COMENTARIOS:    Define material en base a modelo definido por usuario.
"""

# %% [00] INTRODUCTION
# User defined material to adjust the openseespy material into the GUI.

# %% [01] USER DEFINED FUNCTIONS

# %%% [01-00] Saatcioglu (1992)
def Saatcioglu_1992(unit_x, ec, args_x):
    # Unified unit for requirements in User Defined Functions
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
    fco, fl, e01, rho, e085 = args_x  # See data_plot() from S01_GUI02_A02_2_fileText.py. And model_arg() from S01_GUI02_A01_uniaxialMaterial.py. 
    fco, fl, e01, rho, e085 = float(fco), float(fl), float(e01), float(rho), float(e085)
    # Units conversion
    fco = fco * unit_factors_new['MPa'][unit_x]
    fl = fl * unit_factors_new['MPa'][unit_x]

    # 1. Calculate fcc' using Eq (4) or (6):
    k1 = 6.7 * (fl) ** (-0.17)  # where k1 is calculated using Eq (5) or (9)
    fcc = fco + k1 * fl
    # 2. Calculate e1 using Eq (12):
    K = (k1 * fl) / fco  # where K is calculated using Eq (13)
    e1 = e01 * (1 + 5*K)
    # 3. Calculate e85 using Eq (14):
    e85 = 260 * rho * e1 + e085
    # 4. Calculate fc for the parabolic ascending portion using Eq (16):
    if ec <= e1:
        fc = fcc * (2*(ec/e1) - (ec/e1)**2) ** (1/(1 + 2*K))
        if fc > fcc:
            fc = fcc
    # 5. Calculate fc for the linear descending segment:
    else:
        fc = fcc * (1 - 0.15/(e85 - e1) * (ec - e1))
    # 6. Calculate residual strength:
        if fc < 0.2 * fcc:
            fc = 0.2 * fcc
    return fc * unit_factors_new[unit_x]['MPa']  # Return to the original system of units.


# %%% [01-01] Mander (1988)
def Mander_1988(unit_x, ec, args_x):
    fco, CSR, eco, Ec = args_x  # See data_plot() from S01_GUI02_A02_2_fileText.py. And model_arg() from S01_GUI02_A01_uniaxialMaterial.py. 
    fco, CSR, eco, Ec = float(fco), float(CSR), float(eco), float(Ec)

    # 1. Calculate fcc using CSR:
    fcc = CSR * fco
    # 2. Calculate ecc using Eq (5):
    ecc = eco * (1 + 5*(CSR - 1))
    # 3. Calculate Esec using Eq (8):
    Esec = fcc/ecc
    # 4. Calculate r using Eq (6):
    r = Ec / (Ec - Esec)
    # For each value of ec, steps 5 and 6 are repeated:
    # 5. Calculate x using Eq (4):
    x = ec / ecc
    # 6. Calculate fc using Eq (3):
    fc = (fcc * x * r) / (r - 1 + x**r)
    return fc


# %%% [01-02] Belarbi (1994)
def Belarbi_1994(unit_x, ec, args_x):
    # Unified unit for requirements in User Defined Functions
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
    fcr, eps_cr, Ecr = args_x  # See data_plot() from S01_GUI02_A02_2_fileText.py. And model_arg() from S01_GUI02_A01_uniaxialMaterial.py. 
    fcr, eps_cr, Ecr = float(fcr), float(eps_cr), float(Ecr)
    
    # Units conversion
    fcr = fcr * unit_factors_new['MPa'][unit_x]
    Ecr = Ecr * unit_factors_new['MPa'][unit_x]
    
    # 1. Calculate fc:
    if ec <= eps_cr:
        fc = Ecr * ec
    else:
        fc = fcr * ((eps_cr)/(ec)) ** 0.4
    
    return fc * unit_factors_new[unit_x]['MPa']  # Return to the original system of units.
