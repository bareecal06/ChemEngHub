# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 21:34:04 2026

@author: baree
"""
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from calculations import(Reynolds_Number, pressure_drop, pump_power, heat_duty, lmtd, heat_exchange_area, arrhenius, CSTR_volume, PFR_volume,)

st.title("ChemEng Hub")
#Fluid dynamics section

page = st.sidebar.selectbox(
    "Choose Calculator",
    [
        "Reynolds Number",
        "Pressure Drop",
        "Pump Power" ,
        "Heat Duty" ,
        "LMTD Calculator" ,
        "Heat exchange Area",
        "Arrhenius Equation",
        "CSTR Volume",
        "PFR Volume",
        "Reaction Kinetics Simulator",
    ]
)
#Reynolds number calculator
if page == "Reynolds Number":

    st.header("Reynolds Number Calculator")

    rho = st.number_input("Density (kg/m³)", value=1000.0)
    velocity = st.number_input("Velocity (m/s)", value=2.0)
    diameter = st.number_input("Diameter (m)", value=0.05)
    viscosity = st.number_input("Viscosity (Pa·s)", value=0.001)

    if st.button("Calculate"):

        Re = Reynolds_Number(
            rho,
            velocity,
            diameter,
            viscosity
        )
        st.metric("Reynolds Number", f"{Re:.0f}")

        if Re < 2300:
            st.success("Laminar Flow")

        elif Re < 4000:
            st.warning("Transitional Flow")

        else:
            st.error("Turbulent Flow")
            
# Pressure drop calculator
elif page == "Pressure Drop":

    st.header("Pressure Drop Calculator")

    friction_factor = st.number_input(
        "Friction Factor",
        value=0.02,
        format="%.3f"
    )

    length = st.number_input(
        "Pipe Length (m)",
        value=10.0
    )

    diameter2 = st.number_input(
        "Pipe Diameter (m)",
        value=0.05
    )

    density2 = st.number_input(
        "Fluid Density (kg/m³)",
        value=1000.0
    )

    velocity2 = st.number_input(
        "Fluid Velocity (m/s)",
        value=2.0
    )

    if st.button("Calculate Pressure Drop"):

        dp = pressure_drop(
            friction_factor,
            length,
            diameter2,
            density2,
            velocity2
        )

        st.write(f"Pressure Drop = {dp:.2f} Pa")

        if dp < 1000:
            st.success("Low pressure loss")

        elif dp < 10000:
            st.warning("Moderate pressure loss")

        else:
            st.error("High pressure loss - consider increasing pipe diameter or reducing flow velocity.") 
   

#Pump power calculator 
elif page == "Pump Power":

    st.header("Pump Power Calculator")

    flow_rate = st.number_input(
        "Flow Rate (m³/s)",
        value=0.01,
        key="flow_rate"
    )

    head = st.number_input(
        "Pump Head (m)",
        value=20.0,
        key="head"
    )

    density3 = st.number_input(
        "Fluid Density (kg/m³)",
        value=1000.0,
        key="pump_density"
    )

    efficiency = st.number_input(
        "Pump Efficiency",
        min_value=0.01,
        max_value=1.00,
        value=0.80,
        key="efficiency"
    )  

    if st.button("Calculate Pump Power"):

        power = pump_power(
            flow_rate,
            head,
            density3,
            efficiency
        )

        st.metric("Pump Power", f"{power:.2f} W")
        if power < 1000:
            st.success("Suitable for a small pump.")

        elif power < 10000:
            st.warning("Medium-duty pump required.")

        else:
            st.error("High power requirement - check the design conditions.")    
    
# Heat Duty calculation
elif page == "Heat Duty":

    st.header("Heat Duty Calculator")

    mass_flow = st.number_input(
        "Mass Flow Rate (kg/s)",
        value=2.0,
        key="mass_flow"
    )

    cp = st.number_input(
        "Specific Heat Capacity (J/kg·K)",
        value=4180.0,
        key="cp"
    )

    inlet_temp = st.number_input(
        "Inlet Temperature (°C)",
        value=20.0,
        key="Tin"
    )

    outlet_temp = st.number_input(
        "Outlet Temperature (°C)",
        value=80.0,
        key="Tout"
    )

    if st.button("Calculate Heat Duty"):

        Q = heat_duty(
            mass_flow,
            cp,
            inlet_temp,
            outlet_temp
        )

        st.metric(
            "Heat Duty",
            f"{Q/1000:.2f} kW"
        )

        if Q > 0:
            st.success("The fluid is being heated.")

        elif Q < 0:
            st.info("The fluid is being cooled.")

        else:
            st.warning("No heat transfer.")
            

# LMTD Calculator
elif page == "LMTD Calculator":

    st.header("LMTD Calculator")

    st.write("Calculate the Log Mean Temperature Difference for a heat exchanger.")

    delta_t1 = st.number_input(
        "Temperature Difference at End 1 (°C)",
        value=60.0,
        min_value=0.01,
        key="dt1"
    )

    delta_t2 = st.number_input(
        "Temperature Difference at End 2 (°C)",
        value=30.0,
        min_value=0.01,
        key="dt2"
    )

    if st.button("Calculate LMTD"):

        result = lmtd(delta_t1, delta_t2)

        st.metric(
            "LMTD",
            f"{result:.2f} °C"
        )

        if result > 50:
            st.success("Large driving force for heat transfer.")

        elif result > 20:
            st.info("Moderate temperature driving force.")

        else:
            st.warning("Small driving force. A larger heat exchanger may be required.")
        
# Heat Exchanger Area Calculator
elif page == "Heat exchange Area":

    st.header("Heat Exchanger Area")

    lmtd_value = st.number_input(
        "LMTD (°C)",
        value=30.0,
        key="area_lmtd"
    )

    overall_U = st.number_input(
        "Overall Heat Transfer Coefficient (W/m²K)",
        value=500.0,
        key="overall_u"
    )

    heat_duty_value = st.number_input(
        "Heat Duty (W)",
        value=100000.0,
        key="heat_duty_area"
    )

    if st.button("Calculate Heat Exchanger Area"):

        area = heat_exchange_area(
            heat_duty_value,
            overall_U,
            lmtd_value
        )

        st.metric(
            "Required Heat Exchanger Area",
            f"{area:.2f} m²"
        )
    
#Arrehius Calculation
elif page == "Arrhenius Equation":

    st.header("Arrhenius Equation Calculator")

    A = st.number_input(
        "Pre-exponential Factor (1/s)",
        value=1e10,
        format="%.2e",
        key="A"
    )

    Ea = st.number_input(
        "Activation Energy (J/mol)",
        value=50000.0,
        key="Ea"
    )

    T = st.number_input(
        "Temperature (K)",
        value=350.0,
        key="Temp"
    )

    if st.button("Calculate Rate Constant"):

        k = arrhenius(A, Ea, T)

        st.metric(
            "Rate Constant (k)",
            f"{k:.4e} 1/s"
        )

        if T < 300:
            st.info("Low temperature - slower reaction expected.")

        elif T < 500:
            st.success("Moderate reaction conditions.")

        else:
            st.warning("High temperature - reaction rate increases significantly.")

#CSTR Volume
elif page == "CSTR Volume":
    
    st.header("CSTR Volume Calculator")
    
    FA0 = st.number_input(
        "Inlet Molar Flow rate (mol/s)",
        value= 20,
        key = "FA0",
        )
    
    conversion = st.number_input(
        "conversion",
        min_value= 0.0,
        max_value= 1.0,
        key= "conversion",
        )
    
    reaction_rate = st.number_input(
        "Reaction rate (mols/m³·s)",
        value=2,
        )
    if st.button("Calculate CSTR Volume"):
    
        volume = CSTR_volume(
            FA0,
            conversion,
            reaction_rate
        )
    
        st.metric(
            "Required Reactor Volume",
            f"{volume:.2f} m³"
        )

#PFR volume calculator
elif page == "PFR Volume":
    
    st.header("PFR Volume calculator")
    
    FA0_PFR = st.number_input(
        "Inlet Molar Flow rate (mol/s)",
        value= 20,
        key= "FA0_PFR",
        )
    
    conversion_PFR = st.number_input(
        "Conversion",
        min_value=0.0,
        max_value=1.0,
        key= "conversion_PFR",
        )
    
    inlet_conc = st.number_input(
        "Inlet Concentration (mol/m³)",
        value = 100,
        key="concentration",
        )
    rate_constant = st.number_input(
        "Rate constant (1/s)",
        value= 0.1,
        key="rate constant",
        )

    if st.button("PFR Volume"):
        volume = PFR_volume(
        FA0_PFR,
        rate_constant,
        inlet_conc,
        conversion_PFR)
        st.metric(
            "Required Reactor Volume",
            f"{volume:.2f} m³"
        )
        
#Reaction Kinetics PLot
elif page == "Reaction Kinetics Simulator": 

    st.header("Reaction Kinetics Simulator") 

    CA0 = st.number_input( 
        "Initial Concentration (mol/m³)", 
        value=100.0, 
        key="CA0_sim" 
    ) 
     
    k = st.number_input( 
        "Rate Constant (1/s)", 
        value=0.10, 
        format="%.3f", 
        key="k_sim" 
    ) 
     
    simulation_time = st.number_input( 
        "Simulation Time (s)", 
        value=50.0, 
        key="time_sim" 
    ) 

    if st.button("Run Simulation"): 

        # Create time values
        time = np.linspace( 
            0, 
            simulation_time, 
            100
        ) 

        # Calculate concentration
        concentration = CA0 * np.exp(-k * time) 

        # Create graph
        fig, ax = plt.subplots() 

        ax.plot(time, concentration) 

        ax.set_title("Reaction Kinetics Simulation") 
        ax.set_xlabel("Time (s)") 
        ax.set_ylabel("Concentration (mol/m³)") 
        ax.grid(True) 

        st.pyplot(fig) 

        # Final concentration
        st.metric( 
            "Final Concentration", 
            f"{concentration[-1]:.2f} mol/m³"
        )

        # Calculate conversion
        conversion = (1 - concentration[-1] / CA0) * 100
        st.metric(
            "Final Conversion",
            f"{conversion:.1f}%"
        )

                                

   