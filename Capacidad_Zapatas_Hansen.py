# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 09:08:30 2021

@author: JUANK
"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
from math import *
pi = 4 * atan(1)
def cot(x):
    return 1.0/tan(x)

##---------------------DEFINICIÓN DE LA FUNCIÓN--------------------------------
def  Q_ult(B , L, Df, eta, beta, V, H, eB, eL, gamma_s, gamma_sD, phi, cp, cu):    
    ##Sobrecarga --------------------------------------------------------------
    q = gamma_sD * Df
    ##Ángulos a Radianes ------------------------------------------------------
    def cot(x):
        return 1.0/tan(x)
    ##-------------------------------------------------------------------------
    if phi == 0:
        phi == 0.00001
    else:
        phi == phi
    ##-------------------------------------------------------------------------        
    phi_r = phi * pi/180
    eta_r = eta * pi /180
    beta_r = beta * pi /180
    ## Área efectiva-----------------------------------------------------------
    Bp = B - 2 * eB
    Lp = L - 2 * eL
    Af = Bp * Lp
    ##Factores de capacidad de carga
    Nq = exp(pi*tan(phi_r))*pow((tan(pi/4 + phi_r/2)),2)
    Nc = (Nq-1)*cot(phi_r)
    N_gamma = 1.5*(Nq-1)*tan(phi_r)
    ##Factores de inclinación de carga-----------------------------------------
    ca = 0.6 * cp 
    if 0.7* H > (V + Af * ca * cot(phi_r)):
         sys.exit("Condición Drenada - Falla por deslizamiento en la base, verifique cargas y dimensiones")
    else:
        i_q = pow ((1 - 0.5 * H / (V + Af * ca * cot(phi_r))), 5)
    i_c = i_q - (1 - i_q)/(Nq - 1)
    i_gamma = pow ((1 - 0.7 * H / (V + Af * ca * cot(phi_r))),5)
    ## Factores inclinación de la base y terreno-------------------------------
    g_c = 1 - beta/147;
    g_q = 1 - 0.5*tan(beta_r)
    g_gamma = g_q
    b_c = 1 - eta/147
    b_q = exp(-2* eta_r * tan(phi_r))
    b_gamma = exp(-2.7* eta_r * tan(phi_r))
    ## Factores de Forma-------------------------------------------------------
    s_c = 1+ i_c * Nq/Nc * Bp/Lp
    s_q = 1 + i_q * Bp/Lp * sin(phi_r)
    s_gamma = 1 - i_q * 0.4 * Bp/Lp
    if s_gamma < 0.6:
        s_gamma = 0.6
    else:
        s_gamma = s_gamma
    ##Factores de profundidad--------------------------------------------------
    if Df <= B:
        k = Df/B
    else: 
        k = atan (Df/B)
    d_c = 1+ 0.4* k
    d_q = 1 + 2* tan(phi_r) * pow((1- sin(phi_r)),2) * k
    d_gamma = 1
    ## Capacidad Portante Drenada----------------------------------------------
    F1 = s_c * d_c * i_c * g_c * b_c
    F2 = s_q * d_q * i_q * g_q * b_q
    F3 = s_gamma * d_gamma * i_gamma * g_gamma * b_gamma
    T1 = cp * Nc * F1
    T2 = q * Nq * F2
    T3 = 0.5 * gamma_s * Bp * N_gamma * F3
    Q_ult_d = T1 + T2 + T3 ## kPa
    ##-------------------------------------------------------------------------
    print ("Condición drenada")
    print ("Q_ult_d = ", Q_ult_d, "kPa")
    ##-------------------------------------------------------------------------
    ##------------------NO DRENADA---------------------------------------------
    ##Factor de inclinación de carga
    ca_u = 0.6 * cu
    if H > Af*ca_u:
         sys.exit("Condición No Drenada - Falla por deslizamiento en la base, verifique cargas y dimensiones")
    else:
        i_ca = 0.5 - 0.5  * sqrt(1-H/(Af*ca_u))
    ##Factor de forma
    d_ca = 0.4*k
    s_ca = 0.2* i_ca * Bp/Lp
    ##Factor de profundidad
    if Df <= B:
        k = Df/B
    else:
        k = atan (Df/B)
    ##Factores inclinación de la base y terreno
    g_ca = beta/147;
    b_ca = eta/147;
    ## Capacidad Portante No Drenada-------------------------------------------
    Fu = 1 + s_ca + d_ca - i_ca - g_ca - b_ca
    Q_ult_u = (pi + 2) * cu * Fu + q
    ##-------------------------------------------------------------------------
    print ("Condición No drenada")
    print ("Q_ult_u = ", Q_ult_u, "kPa")