# -*- encoding: utf-8 -*-
from django import forms
from .models import User
import re

class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """

    email = forms.EmailField(widget=forms.TextInput,label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Confirmar password")
    #Agregados 3 formularios --------------------------------------------------
    nombre =forms.CharField(widget=forms.TextInput,max_length=120,label="Nombre")
    apellido_paterno=forms.CharField(widget=forms.TextInput,max_length=120)
    apellido_materno=forms.CharField(widget=forms.TextInput,max_length=120)
    #--------------------------------------------------------------------------------
    
    class Meta:
        model = User
        fields = ['nombre', 'apellido_paterno', 'apellido_materno','email', 'password1', 'password2', 'fecha_de_nacimiento', 'genero']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Las contraseñas no coinciden, intenta nuevamente.")
        
        #Validacion tipos de datos en formulario --------------------------------------------------------------------------
        patron = re.compile('\d+') # Patron para buscar numeros en una cadena
        #Validacion nombre 
        if 'nombre' in self.cleaned_data:
            if patron.match(self.cleaned_data['nombre']):
                raise forms.ValidationError("No se admiten numeros en su nombre")
                print "Registro: Error en nombre"
        #Validacion apellido Pat
        if 'apellido_paterno' in self.cleaned_data:
            if patron.match(self.cleaned_data['apellido_paterno']):
                raise forms.ValidationError("No se admiten numeros en sus apellidos")
                print "Registro: Error en Apellido paterno"
        #Validacion apellido Mat
        if 'apellido_materno' in self.cleaned_data:
            if patron.match(self.cleaned_data['apellido_materno']):
                raise forms.ValidationError("No se admiten numeros en sus apellidos")
                print "Registro: Error en Apellido Materno"
        #------------------------------------------------------------------------------------------
        return self.cleaned_data  
    

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user




class RegistrationFormAnalista(forms.ModelForm):
    """
    Form for registering a new account.
    """
    email = forms.EmailField(widget=forms.TextInput,label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Confirmar password")


    class Meta:
        model = User
        fields = ['nombre', 'apellido_paterno', 'apellido_materno','email', 'password1', 'password2', 'fecha_de_nacimiento', 'genero']

    def clean(self):
        """
        Verifies that the values entered into the password fields match

        NOTE: Errors here will appear in ``non_field_errors()`` because it applies to more than one field.
        """
        cleaned_data = super(RegistrationFormAnalista, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Su password no coincide, intente nuevamente.")
        return self.cleaned_data

    def save(self, commit=True, jefe=None):
        self.instance.jefe = jefe
        user = super(RegistrationFormAnalista, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']
