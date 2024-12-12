# -*- coding: utf-8 -*-
"""
ACTUALIZACION:  2024-06-04
AUTOR:          Marcelo Ortiz Á.
SCRIPT:         S01_GUI02_A04_testUniaxialMaterial.py
COMENTARIOS:    Define material a testear en openseespy.
"""

# %% [00] INTRODUCTION
# Para determinar el nivel de esfuerzo para cierto nivel de deformación,
# es necesario limpiar el modelo opensees, definir un material, e indicar que
# se realizara un test al material. Esto se debe repetir diferentes veces,
# por lo que se ejecutaran estas lineas de codigo desde este script, en
# atencion a extension original del codigo.


# %% [01] CODE
ops.wipe()

# Select the correct MatTag
model, MatTag = model_args_x[:2]
MatTag = int(MatTag)
# If there is a MinMax material. Use the other mat tag. It is necessary because in the GUI the material tipe in the widgets is the same for the minmax material
if len(min_max_args_x) != 0:
    OtherTag_minmax = min_max_args_x[2]
    OtherTag_minmax = int(OtherTag_minmax)
    MatTag = OtherTag_minmax

# Define material opensees
if model == 'ConcreteCM':
    fpcc, epcc, Ec, rc, xcrn, ft, et, rt, xcrp, GapClose = model_args_x[2:]
    fpcc, epcc, Ec, rc, xcrn, ft, et, rt, xcrp, GapClose = float(fpcc), float(epcc), float(
        Ec), float(rc), float(xcrn), float(ft), float(et), float(rt), float(xcrp), int(GapClose)
    ops.uniaxialMaterial('ConcreteCM', MatTag, fpcc, epcc, Ec, rc, xcrn, ft, et, rt, xcrp, '-GapClose', GapClose)

elif model == 'Concrete07':
    fc, epsc, Ec, ft, et, xp, xn, r = model_args_x[2:]
    fc, epsc, Ec, ft, et, xp, xn, r = float(fc), float(epsc), float(Ec), float(ft), float(
        et), float(xp), float(xn), float(r)
    ops.uniaxialMaterial('Concrete07', MatTag, fc, epsc, Ec, ft, et, xp, xn, r)

elif model == 'SteelMPF':
    fyp, fyn, E0, bp, bn, R0, cR1, cR2, a1, a2, a3, a4 = model_args_x[2:]
    fyp, fyn, E0, bp, bn, R0, cR1, cR2, a1, a2, a3, a4 = float(fyp), float(fyn), float(E0), float(
        bp), float(bn), float(R0), float(cR1), float(cR2), float(a1), float(a2), float(a3), float(a4)
    ops.uniaxialMaterial('SteelMPF', MatTag, fyp, fyn, E0, bp, bn, R0, cR1, cR2, a1, a2, a3, a4)

elif model == 'Steel02':
    Fy, E0, b, R0, cR1, cR2, a1, a2, a3, a4, sigInit = model_args_x[2:]
    Fy, E0, b, R0, cR1, cR2, a1, a2, a3, a4, sigInit = float(Fy), float(E0), float(b), float(
        R0), float(cR1), float(cR2), float(a1), float(a2), float(a3), float(a4), float(sigInit)
    ops.uniaxialMaterial('Steel02', MatTag, Fy, E0, b, R0, cR1, cR2, a1, a2, a3, a4, sigInit)

elif model == 'Steel01':
    Fy, E0, b, a1, a2, a3, a4 = model_args_x[2:]
    Fy, E0, b, a1, a2, a3, a4 = float(Fy), float(E0), float(b), float(
        a1), float(a2), float(a3), float(a4)
    ops.uniaxialMaterial('Steel01', MatTag, Fy, E0, b, a1, a2, a3, a4)

# If there ia a MinMax material
if len(min_max_args_x) != 0:
    mat_type_minmax, matTag_minmax, OtherTag_minmax, minStrain, maxStrain = min_max_args_x
    matTag_minmax, OtherTag_minmax, minStrain, maxStrain = int(matTag_minmax), int(OtherTag_minmax), float(minStrain), float(maxStrain)
    ops.uniaxialMaterial('MinMax', matTag_minmax, OtherTag_minmax, '-min', minStrain, '-max', maxStrain)
    
    ops.testUniaxialMaterial(matTag_minmax)
    

else:
    ops.testUniaxialMaterial(MatTag)

# %%
