from django.db import models
from django.forms import ModelForm

# Create your models here.

class Graph(models.Model):
    language = model.CharField(max_length=7,choices=[('Python':'Python'),('D','D')])
    ep_model = models.CharField(max_length=50, choices=[('sir','SIR'),('sir_dem','SIR_DEM')])
    column = models.CharField(max_length=16,choices=[('S','Suscetíveis'),('I','Infecciosos')])
    data_alpha = models.DecimalField(max_digits=4,decimal_places=2)
    data_beta = models.DecimalField(max_digits=3,decimal_places=2)
    data_gama = models.CharField(max_length=200,null=False)
    data_pop = models.PositiveIntegerField() #valor de N
    data_i0 = models.PositiveIntegerField()
    data_tf= models.CharField(max_length=5,null=False)

class ep_modelform(ModelForm):

    class Meta:
        model = Graph
        fields = ['language','ep_model', 'column','data_alpha', 'data_beta','data_gama','data_pop','data_i0','data_tf']
        labels = {
            'language': 'Linguagem',
            'ep_model': 'Modelo',
            'column': 'Coluna',
            'data_alpha': "Parâmetro Alpha (apenas para modelo SIR_Dem)",
            'data_beta': "Parâmetro Beta",
            'data_gama': "Parâmetro Gama",
            'data_pop': "População Inicial (N)",
            'data_i0': "Quantidade Inicial de Infecciosos (I0)",
            'data_tf': "Duração da Simulação (dias)"
        }

    def exists_slash(strvar):
        for letter in strvar:
            if letter == '/':
                return True
        return False

