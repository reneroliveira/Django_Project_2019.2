import numpy as np
from scipy.integrate import odeint
from numpy.random import rand, gamma, exponential, poisson
#import pylab as P
#código modificado para melhor implementação de views.py

def run_sir(N, tf, *pars):
    """
    Runs simulation.

    :parameters:
    :param N: tamanho da população
    :param tf: tempo final
    :param nsims:  Numero de simulações
    :param pars: parametros
    """
    beta, gam, I0 = pars
    betat = lambda t: beta + (0.5 * beta) * np.cos((2 * np.pi * t) / 365.)

    t = [0]
    S = [N - I0]
    I = [I0]
    dts = []
    while I[-1] > 0 and t[-1] < tf:
        U = rand()
        # Probabilidade de que pelo menos um evento ocorra
        R = beta * S[-1] * I[-1] / N + gam * I[-1]
        # Probabilidade do próximo evento ser uma infecção
        pinf = ((beta / N) * S[-1] * I[-1]) / R

        if U <= pinf:  # próximo evento é uma infecçao
            dt = exponential(1 / R)

            S.append(S[-1] - 1)
            I.append(I[-1] + 1)
            t.append(t[-1] + dt)
            dts.append(dt)
        else:  # próximo evento é uma recuperação
            S.append(S[-1])
            I.append(I[-1] - 1)
            # print('removal')
            t.append(t[-1] + exponential(1 / R))  # -np.log(rand())/R)
    sims = (np.array([t, S, I]).T, np.array(t), dts)
    # P.plot(t, I, label='$O_t^{}$'.format(k + 1), drawstyle='steps-post')
    return sims


if __name__ == "__main__":
    beta = 0.1
    gam = 1 / 21
    N = 1500
    Tmed = 20
    constant = False
    I0 = 2
    tf = 365
    ts = np.arange(tf)
    nsims = 5
    x = run_sir(N, tf, *(beta, gam, I0))
    # P.plot(x[0][0], x[0][2], label='Infected', drawstyle='steps-post')
    print(x[0])
    # P.legend(loc=0)
    # P.xlabel("t (dias)")
    # P.ylabel("casos")
    # P.grid()
    # P.savefig('simulacao.png')

    P.show()
