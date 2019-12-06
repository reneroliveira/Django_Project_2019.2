from django.shortcuts import render, HttpResponse, render_to_response
from django.views import generic
from .models import Graph, ep_modelform
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components

try:
    import epidemiad
    language='D'
except ImportError:
    from . import epidemia
    language='Python'


def index(request):
    #return HttpResponse("Hello, world. You're at the epid_graph index.")
    context = {'Models': {'SIR': 'sir', 'SIR_Dem': 'sir_dem'},
               'Column':{'Susceptible':'S','Infected':'I','Recovered':'R','All of them':'ALL'},
               'script': "",
               'div': ""
               }
    if request.method == 'GET':
        context['titulo'] = "Choose a model and a column"
        context['form'] = ep_modelform()
    elif request.method == 'POST':
        form = ep_modelform(request.POST)
        context['form'] = form
        if True:
            model = request.POST.get('ep_model', 'sir')
            column = request.POST.get('column','I')
            alpha = request.POST.get('data_alpha',[0.1])
            beta = request.POST.get('data_beta',[0.17])
            gama = request.POST.get('data_beta',['1/21.'])
            N = request.POST.get('data_pop',[15000])
            I0 = request.POST.get('data_i0',[2])
            tf = request.POST.get('data_tf',[365.0])
            #g = Grafico(tipo=tipo, dadosx=x, dadosy=y)
            #g.save()
            script, div = create_graph(model,column,alpha,beta,gama,N,I0,tf)
            context.update({'titulo': "Seu gráfico!",
                            'script': script,
                            'div': div
                            })
        else:
            print(form.is_valid())
            pass

    return render(request, 'home.html', context)


def create_graph(model,col,alpha,beta,gama,N,I0,tf):
    alpha=float(alpha)
    beta = float(beta)
    if ep_modelform.exists_slash(gama):
        g = [float(i) for i in gama.strip('/').split('/')]
        gama2 = g[0] / g[1]
    else:
        gama2 = float(gama)
    gama=gama2
    N=int(N)
    I0=int(I0)
    tf=float(tf)
    print(type(beta),type(gama))
    if language=='D' and model=='sir':
        SIR_model = epidemiad.SIR(N, beta, gama)
        SIR_model.initialize(N - I0, I0, 0)
        sim_dlang = SIR_model.run(0, tf)
    elif language=='D' and model=='sir_dem':
        model_SIRdem = epidemiad.SIR_Dem(N, alpha, beta, gama)
        model_SIRdem.initialize(N - I0, I0, 0)
        sim2_dlang = model_SIRdem.run(0, tf)
    elif language == "Python" and model=='sir':
        sim_dlang=epidemia.run_sir(N, tf, 1, *(beta, gama, I0, 20, False))



    if col == 'I':
        plot = figure(title="Sir_Model", x_axis_label='Tempo (dias)', y_axis_label='Y', plot_width=600, plot_height=400)
        print(len(sim_dlang[0]))
        plot.line(sim_dlang[0][0].tolist(), sim_dlang[0][2], line_width=2)
    '''else:
        plot = figure(title="Grafico de Barras", x_axis_label='X', y_axis_label='Y', plot_width=800, plot_height=400)
        plot.vbar(x=x, width=0.9, top=y, bottom=0)'''

    script, div = components(plot)
    return script, div


'''class GraficoView(generic.ListView):
    template_name = 'grafico_list.html'
    context_object_name = 'lista_de_graficos'''
