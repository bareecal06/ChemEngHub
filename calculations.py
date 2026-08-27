# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 21:34:24 2026

@author: baree
"""

def Reynolds_Number(rho, velocity, diameter, viscosity):
    Re = rho * velocity * diameter / viscosity
    return Re

def pressure_drop(friction_factor, length, diameter, density, velocity):
    dp = friction_factor * (length / diameter) * ((density * velocity**2) / 2)
    return dp

def pump_power(flow_rate, head, density, efficiency):
    g = 9.81
    power = (density * g * flow_rate * head) / efficiency
    return power

def heat_duty(mass_flow_rate, specific_heat, inlet_temp, outlet_temp):
    delta_T = outlet_temp - inlet_temp
    Q = mass_flow_rate * specific_heat * delta_T
    return Q

import math

def lmtd(delta_t1, delta_t2):
    if delta_t1 == delta_t2:
        return delta_t1
    return (delta_t1 - delta_t2) / math.log(delta_t1 / delta_t2)

def heat_exchange_area(heat_duty_value, overall_U, lmtd_value):
    print("NEW FUNCTION LOADED")
    
    area = heat_duty_value / (overall_U * lmtd_value)
    return area

def arrhenius(A, Ea, T):
    R = 8.314
    k = A * math.exp(-Ea / (R * T))
    return k

def CSTR_volume(F_A0, conversion, reaction_rate):
    volume = (F_A0 * conversion) / reaction_rate
    return volume

def PFR_volume(FA0_PFR, conversion_PFR, rate_constant, inlet_conc):
    PFR_volume = ((FA0_PFR / (rate_constant * inlet_conc)) * math.log(1/ (1-conversion_PFR)))
    return PFR_volume