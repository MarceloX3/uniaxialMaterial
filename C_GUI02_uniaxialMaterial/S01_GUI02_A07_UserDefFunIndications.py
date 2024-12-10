# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-06-17
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI02_A07_UserDefFunIndications.py
COMENTARIOS:    Define instructions to use a user defined function in the GUI.
"""

# %% TODO: [00] INTRODUCTION
# Create key for each user defined model with the parameters and units of the model.

# %% TODO: [01] INSTRUCTIONS OF USER DEFINED FUNCTIONS
instructions = {
    'Saatcioglu(1992)': """Paper: STRENGTH AND DUCTILITY OF CONFINED CONCRETE
Authors: Murat Saatcioglu and Salim R. Razvi

Inputs: fco', fle, e01, rho, e085.   Units: [MPa]

1. Calculate fcc' using Eq (4) or (6):
   fcc' = fco' + k1 * fle
   where k1 is calculated using Eq (5) or (9): 
      k1 = 6.7 * (fle)**(-0.17)
2. Calculate e1 using Eq (12):
   e1 = e01 * (1 + 5*K)
   where e01 = Strain corresponding to peak stress of unconfined concrete
      e01 = 0.002, suggested value in the absence of experimental data
   where K is calculated using Eq (13):
      K = (k1 * fle)/(fco')
3. Calculate e85 using Eq (14):
   e85 = 260 * rho * e1 + e085
   where e085 = Strain corresponding to 85% strength of the peak stress of unconfined concrete
         e085 = 0.0038, suggested value in the absence of experimental data
         rho = Transverse reinforcement ratio. Fix a practical upper limit of 2%.
4. Calculate fc for the parabolic ascending portion using Eq (16):
   fc = fcc' * (2*(ec/e1) - (ec/e1)**2) ** (1/(1 + 2*K))
      with fc <= fcc'
5. Calculate fc for the linear descending segment:
   fc = fcc' * (1 - m * (ec - e1))
   where m = (0.15)/(e85 - e1)
      with fc >= 0.2*fcc'
6. Calculate residual strength:
   fc = 0.2 * fcc'
""",
    'Mander(1988)': """Paper: THEORETICAL STRESS-STRAIN MODEL FOR CONFINED CONCRETE
Authors: John B. Mander, Michael J. N. Priestley, and Richard Park

Inputs: fco', CSR, eco, Ec
Note: CSR = confined strength ratio = fcc'/fco'

1. Calculate fcc using CSR:
   fcc = CSR * fco
   where fco = Peak stress of unconfined concrete    
2. Calculate ecc using Eq (5):
   ecc = eco * (1 + 5*(CSR - 1))
   where eco = Strain corresponding to peak stress of unconfined concrete
        eco = 0.002, suggested value in the absence of experimental data
3. Calculate Esec using Eq (8):
   Esec = fcc/ecc
4. Calculate r using Eq (6):
    r = Ec / (Ec - Esec)
For each value of ec, steps 5 and 6 are repeated:
    5. Calculate x using Eq (4):
       x = ec / ecc
    6. Calculate fc using Eq (3):
       fc = (fcc * x * r) / (r - 1 + x**r)
""",
    'Belarbi(1994)': """Paper: CONSTITUTIVE LAWS OF CONCRETE IN TENSION AND REINFORCING BARS STIFFENED BY CONCRETE
Authors: A. Belarbi, T. Hsu

Inputs: fcr, eps_cr, Ecr

Image: L. M. Massone
"""
}
