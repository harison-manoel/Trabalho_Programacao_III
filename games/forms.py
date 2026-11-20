from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Jogo, Avaliacao


class UsuarioCadastroForm(UserCreationForm):
    """
    Formulário para inscrição de novos usuários no site.
    Atende ao Requisito 2: 'O usuário deverá poder se inscrever no seu site.'
    """
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label="Nome Completo",
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-dark',
            'placeholder': 'Seu nome completo'
        })
    )
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-dark',
            'placeholder': 'seuemail@exemplo.com'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-dark',
            'placeholder': 'Escolha um nome de usuário (gamer tag)'
        })
        self.fields['username'].help_text = "Obrigatório. Até 150 caracteres. Letras, dígitos e @/./+/-/_ apenas."
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control form-control-dark',
                'placeholder': 'Digite uma senha segura'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control form-control-dark',
                'placeholder': 'Confirme sua senha'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado em outra conta.")
        return email


class JogoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de jogos.
    Exige autenticação para uso.
    """
    class Meta:
        model = Jogo
        fields = [
            'titulo',
            'categoria',
            'desenvolvedora',
            'distribuidora',
            'plataforma',
            'data_lancamento',
            'preco',
            'descricao',
            'imagem',
            'imagem_url',
            'trailer_url',
            'site_oficial',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Ex: The Witcher 3: Wild Hunt'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select form-control-dark'
            }),
            'desenvolvedora': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Ex: CD Projekt Red, FromSoftware'
            }),
            'distribuidora': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Ex: Bandai Namco, Sony Interactive'
            }),
            'plataforma': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Ex: PC, PlayStation 5, Xbox Series X/S, Nintendo Switch'
            }),
            'data_lancamento': forms.DateInput(attrs={
                'class': 'form-control form-control-dark',
                'type': 'date'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'form-control form-control-dark',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control form-control-dark',
                'rows': 5,
                'placeholder': 'Escreva a sinopse, mecânicas e pontos fortes do jogo...'
            }),
            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control form-control-dark'
            }),
            'imagem_url': forms.URLInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'https://exemplo.com/imagem-capa.jpg'
            }),
            'trailer_url': forms.URLInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'https://www.youtube.com/watch?v=...'
            }),
            'site_oficial': forms.URLInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'https://store.steampowered.com/app/...'
            }),
        }


class AvaliacaoForm(forms.ModelForm):
    """
    Formulário para os usuários logados avaliarem os jogos.
    """
    class Meta:
        model = Avaliacao
        fields = ['nota', 'titulo', 'recomenda', 'comentario']
        widgets = {
            'nota': forms.Select(attrs={
                'class': 'form-select form-control-dark'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control form-control-dark',
                'placeholder': 'Resuma sua opinião em uma frase'
            }),
            'recomenda': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'role': 'switch'
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control form-control-dark',
                'rows': 4,
                'placeholder': 'Dê detalhes sobre jogabilidade, gráficos, história e se vale a pena comprar...'
            }),
        }
