# aktiviraj myenv okolje
import pybamm
import pybammeis 
import numpy as np
import matplotlib.pyplot as plt
import time
from ipywidgets import interact, FloatSlider
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Shrani slike
save_fig = False 

# Shrani animacijo
save_ani = False

# Formatiranje grafov
# Nastavitev velikosti grafa (širina, višina v inch-ih)
fig_size = figsize=(8, 6)  

# Nastavitev velikosti pisave
plt.rcParams.update({
    'font.size': 20,           # Osnovna velikost pisave
    'axes.titlesize': 20,      # Velikost naslova grafa
    'axes.labelsize': 20,      # Velikost pisave na osi
    'xtick.labelsize': 18,     # Velikost številk na x osi
    'ytick.labelsize': 18,     # Velikost številk na y osi
    'legend.fontsize': 18,     # Velikost pisave v legendi
})

# model, ki ima le mehansko degradacijo
model_DFN = pybamm.lithium_ion.DFN(options={"surface form": "differential",
                                                  "particle": "Fickian diffusion",
                                                 "particle mechanics": "swelling only",
                                                 },
                                        )

model_DFN2 = pybamm.lithium_ion.DFN(options={"surface form": "differential",
                                                    "particle": "Fickian diffusion",        
                                                    "particle mechanics": "swelling only",
                                                    "intercalation kinetics": "asymmetric Butler-Volmer",
                                                    },
                                        )


param0 = pybamm.ParameterValues("Ai2020") 
param0.update(
    {"Hydrostatic stress [Pa]": 0,
     "Negative electrode Butler-Volmer transfer coefficient":0.5,
     "Positive electrode Butler-Volmer transfer coefficient":0.5},
    check_already_exists=False  
)


param1 = pybamm.ParameterValues("Ai2020") 
param1.update(
    {"Hydrostatic stress [Pa]": 1e9,
     "Negative electrode Butler-Volmer transfer coefficient":0.5,
     "Positive electrode Butler-Volmer transfer coefficient":0.5},
    check_already_exists=False  
)


param2 = pybamm.ParameterValues("Ai2020") 
param2.update(
    {"Hydrostatic stress [Pa]": 2e9,
     "Negative electrode Butler-Volmer transfer coefficient":0.5,
     "Positive electrode Butler-Volmer transfer coefficient":0.5},
    check_already_exists=False  
)


var_pts = {
    "x_n": 30,  # negative electrode
    "x_s": 20,  # separator
    "x_p": 30,  # positive electrode
    "r_n": 25,  # negative particle
    "r_p": 25,  # positive particle
}


experiment = pybamm.Experiment(["Discharge at 1C until 3.0 V"])
solver = pybamm.IDAKLUSolver()  


sim_DFN_0 = pybamm.Simulation(model= model_DFN, parameter_values=param0, var_pts=var_pts, solver=solver, 
                              experiment=experiment 
                              )
sim_DFN_1 = pybamm.Simulation(model= model_DFN, parameter_values=param1, var_pts=var_pts, solver=solver, 
                              experiment=experiment 
                              )
sim_DFN_2 = pybamm.Simulation(model= model_DFN, parameter_values=param2, var_pts=var_pts, solver=solver, 
                              experiment=experiment 
                              )
sim_DFN2_0 = pybamm.Simulation(model= model_DFN2, parameter_values=param0, var_pts=var_pts, solver=solver,
                               experiment=experiment 
                              )
sim_DFN2_1 = pybamm.Simulation(model= model_DFN2, parameter_values=param1, var_pts=var_pts, solver=solver,
                               experiment=experiment 
                              )
sim_DFN2_2 = pybamm.Simulation(model= model_DFN2, parameter_values=param2, var_pts=var_pts, solver=solver,
                               experiment=experiment 
                              )
######################
t_eval = [0, 3600]
# t_eval = np.arange(0, 3601, 10)  
######################

# start = time.time()
# sol_DFN = sim_DFN_0.solve(t_eval=t_eval)
# end = time.time()
# print(f"Simulacija DFN_0 zaključena v {end - start:.2f} s.")

# start = time.time()
# sol_DFN_1 = sim_DFN_1.solve(t_eval=t_eval)
# end = time.time()
# print(f"Simulacija DFN_1 zaključena v {end - start:.2f} s.")

# start = time.time()
# sol_DFN_2 = sim_DFN_2.solve(t_eval=t_eval)
# end = time.time()
# print(f"Simulacija DFN_2 zaključena v {end - start:.2f} s.")

# start = time.time()
# # data_ox = sim_DFN2_0.solve(t_eval=t_eval)
# sol_DFN2_0 = sim_DFN2_0.solve(t_eval=t_eval)
# end = time.time()
# print(f"Simulacija DFN_2 zaključena v {end - start:.2f} s.")

# start = time.time()
# sol_DFN2_1 = sim_DFN2_1.solve(t_eval=t_eval)
# end = time.time()
# print(f"Simulacija DFN2_1 zaključena v {end - start:.2f} s.")

# start = time.time()
# sol_DFN2_2 = sim_DFN2_2.solve(t_eval=t_eval)    
# end = time.time()
# print(f"Simulacija DFN2_2 zaključena v {end - start:.2f} s.")


eis_sim_DFN = pybammeis.EISSimulation(model= model_DFN, parameter_values= param0)
eis_sim_DFN_1 = pybammeis.EISSimulation(model= model_DFN, parameter_values= param1)
eis_sim_DFN_2 = pybammeis.EISSimulation(model= model_DFN, parameter_values= param2)
eis_sim_DFN_3 = pybammeis.EISSimulation(model= model_DFN2, parameter_values= param0)
eis_sim_DFN_4 = pybammeis.EISSimulation(model= model_DFN2, parameter_values= param1)
eis_sim_DFN_5 = pybammeis.EISSimulation(model= model_DFN2, parameter_values= param2)

# eis_sim.solve(frequencies, inputs={"SOC": z})

frequencies = np.logspace(-4, 4, 30)
eis_sim_DFN.solve(frequencies)
eis_sim_DFN_1.solve(frequencies)
eis_sim_DFN_2.solve(frequencies)
eis_sim_DFN_3.solve(frequencies)
eis_sim_DFN_4.solve(frequencies)
eis_sim_DFN_5.solve(frequencies)

fig, ax = plt.subplots(figsize=(6, 6))

# narišemo Nyquistove diagrame
eis_sim_DFN.nyquist_plot(ax=ax, label="$BV \: \sigma_{\mathrm{h}}=$0 Pa", linestyle="-")
eis_sim_DFN_1.nyquist_plot(ax=ax, label="$BV \: \sigma_{\mathrm{h}}=$1e9 Pa", linestyle="--")
eis_sim_DFN_2.nyquist_plot(ax=ax, label="$BV \: \sigma_{\mathrm{h}}=$2e9 Pa", linestyle="--")
eis_sim_DFN_3.nyquist_plot(ax=ax, label="$exp(ox) \: \sigma_{\mathrm{h}}=$0e9 Pa", linestyle="--")
eis_sim_DFN_4.nyquist_plot(ax=ax, label="$exp(ox) \: \sigma_{\mathrm{h}}=$1e9 Pa", linestyle="--")
eis_sim_DFN_5.nyquist_plot(ax=ax, label="$exp(ox) \: \sigma_{\mathrm{h}}=$2e9 Pa", linestyle="--")


# onemogočimo "enako" merilo osi,
# da figsize=(8,6) dejansko določi razmerje width:height
ax.set_aspect("auto")

# omejimo realni del
ax.set_xlim(0, 0.32)
ax.set_ylim(0, 0.32)

# zdaj prikažemo legendo
ax.legend(loc="center right", bbox_to_anchor=(1.8, 0.5))

#title
ax.set_xlabel("$\mathrm{Z_{Re}}$ [Ω]")
ax.set_ylabel("$\mathrm{-Z_{Im}}$ [Ω]")


if save_fig:
    plt.savefig("graphs/EIS_i0_cel.eps", format='eps', dpi=600, bbox_inches='tight')
plt.show()