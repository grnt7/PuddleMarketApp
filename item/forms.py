from django import forms

from .models import Item


INPUT_CLASSES = 'w-full py-4 px-6 mt-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price',  'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
             'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
             'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        # FIX: fields MUST be here, indented under Meta
        fields = ( 'name', 'description', 'price', 'image', 'is_sold')
        
        # FIX: widgets should also be here
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

    # title = forms.CharField(widget=forms.TextInput(attrs={
    #     'placeholder': 'Item Title',
    #     'class': 'w-full py-4 px-6 rounded-xl'
    # }))

    # description = forms.CharField(widget=forms.Textarea(attrs={
    #     'placeholder': 'Item Description',
    #     'class': 'w-full py-4 px-6 rounded-xl',
    #     'rows': 5
    # }))

    # price = forms.DecimalField(widget=forms.NumberInput(attrs={
    #     'placeholder': 'Item Price',
    #     'class': 'w-full py-4 px-6 rounded-xl'
    # }))

    # category = forms.ModelChoiceField(queryset=None, widget=forms.Select(attrs={
    #     'class': 'w-full py-4 px-6 rounded-xl'
    # }))

    # image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
    #     'class': 'w-full py-4 px-6 rounded-xl'
    # }))

    # def __init__(self, *args, **kwargs):
    #     super(NewItemForm, self).__init__(*args, **kwargs)
    #     from item.models import Category
    #     self.fields['category'].queryset = Category.objects.all()