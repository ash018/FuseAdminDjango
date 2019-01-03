from django import forms
import datetime

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

class ProductForm(forms.Form):
    productName = forms.CharField(label='Product Name',max_length=100)
    productColor = forms.CharField(label='Product Color',max_length=100)
    productPrice = forms.DecimalField(label='Product Price',decimal_places=8,max_digits=10)
    activeDate = forms.DateField(label='Active Date',initial=datetime.date.today)
    bookingPeriod = forms.IntegerField(label='Booking Period')
    bookingPrice = forms.IntegerField(label='Booking Price')
    minimumBookingPrice = forms.DecimalField(label='Minimum Booking Price',decimal_places=8,max_digits=10)
    productImage = forms.FileField(label='Product Image')
    status = forms.CheckboxInput()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'first arg is the legend of the fieldset',
                'like_website',
                'favorite_number',
                'favorite_color',
                'favorite_food',
                'notes'
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='button white')
            )
        )
        super(ProductForm, self).__init__(*args, **kwargs)