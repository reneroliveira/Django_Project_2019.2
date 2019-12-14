from django.shortcuts import render, HttpResponse, render_to_response
from django.views import generic
from .models import Graph, ep_modelform
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

try:
    import epidemiad
    language = 'D'
except ImportError:
    from . import epidemia
    language = 'Python'


def index(request):
    context = {'Models': {'SIR': 'sir', 'SIR_Dem': 'sir_dem'},
               'Column': {'Susceptible': 'S', 'Infected'},
               'script': "",
               'div': ""
               }
    if request.method == 'GET':
        context['titulo'] = "Escolha seu modelo"
        context['form'] = ep_modelform()
    elif request.method == 'POST':
        form = ep_modelform(request.POST)
        context['form'] = form
        model = request.POST.get('ep_model', 'sir')
        column = request.POST.get('column', 'I')
        alpha = request.POST.get('data_alpha', [0.1])
        beta = request.POST.get('data_beta', [0.17])
        gama = request.POST.get('data_gama', ['1/21.'])
        N = request.POST.get('data_pop', [15000])
        I0 = request.POST.get('data_i0', [2])
        tf = request.POST.get('data_tf', [365.0])
        script, div = create_graph(model, column, alpha, beta, gama, N, I0, tf)
        context.update({'titulo': "Simulação",
                        'script': script,
                        'div': div
                        })

    return render(request, 'home.html', context)


def create_graph(model, col, alpha, beta, gama, N, I0, tf):
    alpha = float(alpha)
    beta = float(beta)
    if ep_modelform.exists_slash(gama):
        g = [float(i) for i in gama.strip('/').split('/')]
        gama2 = g[0] / g[1]
    else:
        gama2 = float(gama)
    gama = gama2
    N = int(N)
    I0 = int(I0)
    tf = float(tf)
    print(N,type(N), I0,type(I0),tf,type(tf))
    if language == 'D':
        if model == 'sir':
            print(type(epidemiad.SIR(N, beta, gama)))
            SIR_model = epidemiad.SIR(N, beta, gama)
            SIR_model.initialize(N - I0, I0, 0)
            sim = SIR_model.run(0, tf)
            if col == "I":  ##
                plot = figure(title="Modelo SIR", x_axis_label='Tempo (dias)', y_axis_label='Infectados',
                              plot_width=600,
                              plot_height=400)
                plot.line(sim[0], sim[2], line_width=2)
            elif col == "S":
                plot = figure(title="Modelo SIR", x_axis_label='Tempo (dias)', y_axis_label='Sucetíveis',
                              plot_width=600,
                              plot_height=400)
                plot.line(sim[0], sim[1], line_width=2)
        elif model == 'sir_dem':
            model_SIRdem = epidemiad.SIR_Dem(N, alpha, beta, gama)
            model_SIRdem.initialize(N - I0, I0, 0)
            sim = model_SIRdem.run(0, tf)
            if col == "I":
                plot = figure(title="Modelo SIR_DEM", x_axis_label='Tempo (dias)', y_axis_label='Infectados',
                              plot_width=600,
                              plot_height=400/3)
                plot.line(sim[0], sim[2], line_width=2)
            elif col == "S":
                plot = figure(title="Modelo SIR_DEM", x_axis_label='Tempo (dias)', y_axis_label='Sucetíveis',
                              plot_width=600,
                              plot_height=400/3)
                plot.line(sim[0], sim[1], line_width=2)
    elif language == "Python" and model == 'sir':
        sim = epidemia.run_sir(N, tf, *(beta, gama, I0))
        if col == "I":
            plot = figure(title="Modelo SIR", x_axis_label='Tempo (dias)', y_axis_label='Infectados', plot_width=600,
                          plot_height=400)
            plot.line(sim[0].T[0], sim[0].T[2], line_width=2)
            # plot.line(sim[0].T[0],[N/2]*len(sim[0].T[2]))
        elif col == "S":
            plot = figure(title="Modelo SIR", x_axis_label='Tempo (dias)', y_axis_label='Sucetíveis', plot_width=600,
                          plot_height=400)
            plot.line(sim[0].T[0], sim[0].T[1], line_width=2)

    script, div = components(plot)
    return script, div


