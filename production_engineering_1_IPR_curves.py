import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title('Production Engineering 1')
st.header('IPR Curves')

status = st.radio('What do you want to do', ['Calculations', 'Plot IPR curve'])
if status == 'Calculations':
    question = st.selectbox('What do you want to find? ', ['Reservoir Pressure',
                                                           'Flowing Wellbore Pressure',
                                                           'Flow Rate',
                                                           'Production Index',
                                                           'Maximum Flow Rate'])

    Pres = float(st.text_input('Enter Reservoir Pressure: '))
    Pwf = float(st.text_input('Enter Flowing Wellbore Pressure: '))
    Q = float(st.text_input('Enter Flow Rate'))
    Pb = float(st.text_input('Enter Bubble Pressure'))
    J = float(st.text_input('Enter Productivity Index'))
    Qmax = float(st.text_input('Enter Maximum Flow Rate'))
    condition = 'undersaturated'

    def find_Pres(Pwf, Q, Pb, J):
        pass

    def find_Pwf(Pres, Q, J):
        if condition == 'undersaturated':
            Pwf = (J*Pres - Q) / J
            st.write('Flowing Wellbore Pressure = ', round(Pwf,3))
        elif condition == 'saturated':
            pass
        elif condition == 'halfsaturated':
            pass

    def find_Q(Pres, Pwf, Pb, J, Qmax):
        if Pres > Pwf >= Pb:
            Q =  J * (Pres - Pwf)
            st.write('Flow Rate = ', round(Q,3))
        elif Pb > Pres > Pwf:
            Q = Qmax * (1 - 0.2*(Pwf/Pres) - 0.8*(Pwf/Pres)**2)
            st.write('Flow Rate = ', round(Q, 3))
        elif Pres > Pb > Pwf:
            pass

    def find_Qmax(Pres, Pwf ,Pb, J, Q):
        if Pres > Pwf >= Pb:
            pass
        elif Pb > Pres > Pwf:
            Qmax = Q / (1 - 0.2*(Pwf/Pres) - 0.8*(Pwf/Pres)**2)
            st.write('Maximum Flow Rate = ',round(Qmax,3))
        elif Pres > Pb > Pwf:
            pass

    def find_J(Pres, Pwf, Q, Pb):
        if Pres > Pwf >= Pb:
            J = Q / (Pres - Pwf)
            st.write('Productivity Index = ', round(J,3))
            condition = 'undersaturated'
        elif Pb > Pres > Pwf:
            pass
        elif Pres > Pb > Pwf:
            pass

    if question == 'Reservoir Pressure':
        pass
    elif question == 'Flowing Wellbore Pressure':
        find_Pwf(Pres, Q, J)
    elif question == 'Flow Rate':
        find_Q(Pres, Pwf, Pb, J, Qmax)
    elif question == 'Production Index':
        find_J(Pres, Pwf, Q, Pb)
    elif question == 'Maximum Flow Rate':
        find_Qmax(Pres, Pwf, Pb, J, Q)

elif status == 'Plot IPR curve':
    st.header('IPR curve plotter')
    Pres = float(st.text_input('Enter Reservoir Pressure'))
    Pb = float(st.text_input('Enter Bubble Pressure'))
    Pwf1 = float(st.text_input('Enter Tested Pwf in well A'))
    Q1 = float(st.text_input('Enter Tested Q in well A'))
    Pwf2 = float(st.text_input('Enter Tested Pwf in well B'))
    Q2 = float(st.text_input('Enter Tested Q in well B'))

    if Pwf1 > Pb:
        J1 = Q1 / (Pres - Pwf1)
    else:
        J1 = Q1 / ((Pres - Pb) + (Pb/1.8)*(1-0.2*(Pwf1/Pb) - 0.8*(Pwf1/Pb)**2))
    st.write('J1 = ', round(J1,3))
    if Pwf2 > Pb:
        J2 = Q2 / (Pres - Pwf2)
    else:
        J2 = Q2 / ((Pres - Pb) + (Pb/1.8)*(1-0.2*(Pwf2/Pb) - 0.8*(Pwf2/Pb)**2))
    st.write('J2 = ', round(J2,3))

    Pwf_grid_1 = np.arange(0, Pb, 500).astype(int)
    Pwf_grid_2 = np.arange(Pb, Pres+500, 500).astype(int)
    Pwf_grid = np.concatenate((Pwf_grid_1,Pwf_grid_2))

    Q1_above = J1 * (Pres - Pwf_grid_2)
    Q1_below = J1 * ((Pres - Pb) + (Pb/1.8)*(1-0.2*(Pwf_grid_1/Pb) - 0.8*(Pwf_grid_1/Pb)**2))
    Q1_grid = np.concatenate((Q1_below, Q1_above))

    Q2_above = J2 * (Pres - Pwf_grid_2)
    Q2_below = J2 * ((Pres - Pb) + (Pb/1.8)*(1-0.2*(Pwf_grid_1/Pb) - 0.8*(Pwf_grid_1/Pb)**2))
    Q2_grid = np.concatenate((Q2_below, Q2_above))


    fig, ax = plt.subplots()
    ax.plot(Q1_grid, Pwf_grid)
    ax.set_xlabel('Q - Flow Rate')
    ax.set_ylabel('Pwf - Flowing BH Pressure')

    ax.plot(Q2_grid, Pwf_grid)
    ax.legend(['Well A','Well B'])
    st.pyplot(fig)