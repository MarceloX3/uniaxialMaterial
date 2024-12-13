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

elif model == 'Concrete01':
    fpc, epsc0, fpcu, epsU = model_args_x[2:]
    fpc, epsc0, fpcu, epsU = float(fpc), float(epsc0), float(fpcu), float(epsU)
    ops.uniaxialMaterial('Concrete01', MatTag, fpc, epsc0, fpcu, epsU)

elif model == 'Concrete02':
    fpc, epsc0, fpcu, epsU, lamb, ft, Ets = model_args_x[2:]
    fpc, epsc0, fpcu, epsU, lamb, ft, Ets = float(fpc), float(epsc0), float(
        fpcu), float(epsU), float(lamb), float(ft), float(Ets)
    ops.uniaxialMaterial('Concrete02', MatTag, fpc, epsc0, fpcu, epsU, lamb, ft, Ets)

elif model == 'SteelMPF':
    fyp, fyn, E0, bp, bn, R0, cR1, cR2, a1, a2, a3, a4 = model_args_x[2:]
    fyp, fyn, E0, bp, bn, R0, cR1, cR2, a1, a2, a3, a4 = float(fyp), float(fyn), float(E0), float(
        bp), float(bn), float(R0), float(cR1), float(cR2), float(a1), float(a2), float(a3), float(a4)
    params = [R0, cR1, cR2]
    ops.uniaxialMaterial('SteelMPF', MatTag, fyp, fyn, E0, bp, bn, *params, a1, a2, a3, a4)

elif model == 'Steel02':
    Fy, E0, b, R0, cR1, cR2, a1, a2, a3, a4, sigInit = model_args_x[2:]
    Fy, E0, b, R0, cR1, cR2, a1, a2, a3, a4, sigInit = float(Fy), float(E0), float(b), float(
        R0), float(cR1), float(cR2), float(a1), float(a2), float(a3), float(a4), float(sigInit)
    params = [R0, cR1, cR2]
    ops.uniaxialMaterial('Steel02', MatTag, Fy, E0, b, *params, a1, a2, a3, a4, sigInit)

elif model == 'Steel01':
    Fy, E0, b, a1, a2, a3, a4 = model_args_x[2:]
    Fy, E0, b, a1, a2, a3, a4 = float(Fy), float(E0), float(b), float(
        a1), float(a2), float(a3), float(a4)
    ops.uniaxialMaterial('Steel01', MatTag, Fy, E0, b, a1, a2, a3, a4)

elif model == 'Steel4':
    flag, Fy, E0, b_k, R0, r1, r2, b_kc, R0c, r1c, r2c, b_i, rho_i, b_I, R_i, I_yp, b_ic, rho_ic, b_Ic, R_ic, f_u, R_u, f_uc, R_uc, sig_init, cycNum = model_args_x[2:]
    flag, Fy, E0, b_k, R0, r1, r2, b_kc, R0c, r1c, r2c, b_i, rho_i, b_I, R_i, I_yp, b_ic, rho_ic, b_Ic, R_ic, f_u, R_u, f_uc, R_uc, sig_init, cycNum = str(
        flag), float(Fy), float(E0), float(b_k), float(R0), float(r1), float(r2), float(b_kc), float(R0c), float(r1c), float(r2c), float(b_i), float(rho_i), float(b_I), float(R_i), float(I_yp), float(b_ic), float(rho_ic), float(b_Ic), float(R_ic), float(f_u), float(R_u), float(f_uc), float(R_uc), float(sig_init), int(cycNum)
    params = [R0, r1, r2]
    
    #['-kin', '-iso', '-asym -kin', '-asym -iso', '-kin -ult', '-iso -ult', '-asym -kin -ult', '-asym -iso -ult']
    if flag == '-kin':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-kin', b_k, R0, r1, r2, '-init', sig_init, '-mem', cycNum)
    elif flag == '-iso':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-iso', b_i, rho_i, b_I, R_i, I_yp, '-init', sig_init, '-mem', cycNum)
    elif flag == '-asym -kin':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-asym', '-kin', b_k, R0, r1, r2, b_kc, R0c, r1c, r2c, '-init', sig_init, '-mem', cycNum)
    elif flag == '-asym -iso':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-asym', '-iso', b_i, rho_i, b_I, R_i, I_yp, b_ic, rho_ic, b_Ic, R_ic, '-init', sig_init, '-mem', cycNum)
    elif flag == '-kin -ult':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-kin', b_k, R0, r1, r2, '-ult', f_u, R_u, '-init', sig_init, '-mem', cycNum)
    elif flag == '-iso -ult':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-iso', b_i, rho_i, b_I, R_i, I_yp, '-ult', f_u, R_u, '-init', sig_init, '-mem', cycNum)
    elif flag == '-asym -kin -ult':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-asym', '-kin', b_k, R0, r1, r2, b_kc, R0c, r1c, r2c, '-ult', f_u, R_u, f_uc, R_uc, '-init', sig_init, '-mem', cycNum)
    elif flag == '-asym -iso -ult':
        ops.uniaxialMaterial('Steel4', MatTag, Fy, E0, '-asym', '-iso', b_i, rho_i, b_I, R_i, I_yp, b_ic, rho_ic, b_Ic, R_ic, '-ult', f_u, R_u, f_uc, R_uc, '-init', sig_init, '-mem', cycNum)
    
    
# If there ia a MinMax material
if len(min_max_args_x) != 0:
    mat_type_minmax, matTag_minmax, OtherTag_minmax, minStrain, maxStrain = min_max_args_x
    matTag_minmax, OtherTag_minmax, minStrain, maxStrain = int(matTag_minmax), int(OtherTag_minmax), float(minStrain), float(maxStrain)
    ops.uniaxialMaterial('MinMax', matTag_minmax, OtherTag_minmax, '-min', minStrain, '-max', maxStrain)
    
    ops.testUniaxialMaterial(matTag_minmax)
    

else:
    ops.testUniaxialMaterial(MatTag)

# %%
