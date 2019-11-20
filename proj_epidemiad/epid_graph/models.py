from django.db import models
from django.forms import ModelForm, ValidationError


# Create your models here.

class Graph(models.Model):
    ep_model = models.CharField(max_length=50, choices=[('sir','SIR model'),('sir_dem','SIR model with demography')])
    column = models.CharField(max_length=16,choices=[('S','Susceptible'),('I','Infected'),('R','Recovered'),('ALL','All of them')])
    data_alpha = models.DecimalField(max_digits=12,decimal_places=10)
    data_beta = models.DecimalField(max_digits=11,decimal_places=10)
    data_gama = models.CharField(max_length=200,null=False)
    data_pop = models.PositiveIntegerField() #valor de N
    data_i0 = models.PositiveIntegerField()
    data_tf= models.DecimalField(max_digits=21,decimal_places=15)

class ep_modelform(ModelForm):

    class Meta:
        model = Graph
        fields = ['ep_model', 'column','data_alpha', 'data_beta','data_gama','data_pop','data_i0','data_tf']
        labels = {
            'ep_model': 'Modelo',
            'column': 'Column',
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
    def clean_data_alpha(self):
        data_alpha = self.cleaned_data['data_alpha']

        try:
            alpha = float(data_alpha)
        except:
            raise ValidationError("Formataçao inválida para valor de alpha")
        if beta <0 or beta >1:
            raise ValidationError("Valor de Alpha fora do intervalo [0,1]")
        return data_alpha

    def clean_data_beta(self):
        data_beta = self.cleaned_data['data_beta']

        try:
            float(data_beta)
        except:
            raise ValidationError("Formataçao inválida para valor de beta")
        beta = float(data_beta)
        if beta<0 or beta>1:
            raise ValidationError("Valor de Beta fora do intervalo [0,1]")
        return data_beta
    def clean_data_gama(self):
        data_gama = self.cleaned_data['data_gama']
        try:
            if exists_slash(data_gama):
                g=[float(i) for i in data_gama.strip('/').split('/')]
                gama=g[0]/g[1]
            else:
                gama = float(data_gama)
        except:
            raise ValidationError("Formatação Inválida para o valor de Gama")
        if gama <0:
            raise ValidationError("Valor de Gama deve ser positivo")
        return data_gama

    def clean_data_pop(self):
        data_pop = self.cleaned_data['data_pop']
        try:
            pop = int(data_pop)
        except:
            raise ValidationError("Formataçao inválida para valores de N (população)")
        return data_pop

    def clean_data_i0(self):
        data_i0 = self.cleaned_data['data_i0']
        try:
            i0=int(data_i0)
        except:
            raise ValidationError("Formataçao inválida para valores de I0")
        return data_i0
    def clean_data_tf(self):
        data_tf = self.cleaned_data['data_tf']
        try:
            tf=float(data_tf)
        except:
            raise ValidationError("Formataçao inválida para valores de tf")

