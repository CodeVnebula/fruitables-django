from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Your name',
                'class': 'form-control'
            }
        ),
        max_length=100, 
        required=True,
        error_messages={
            'required': 'Please enter your name.'
        }
    )
    
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Subject',
                'class': 'form-control'
            }
        ),
        max_length=100, 
        required=True,
        error_messages={
            'required': 'Please enter a subject.'
        }
    )
    
    from_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Your email',
                'class': 'form-control'
            }
        ),
        required=True,
        error_messages={
            'required': 'Please enter your email address.'
        }
    )
    
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Your message',
                'class': 'form-control'
            }
        ),
        required=True,
        error_messages={
            'required': 'Please enter your message.'
        }
    )
