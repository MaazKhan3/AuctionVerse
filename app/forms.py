from django import forms

class BidForm(forms.Form):
    bid_amount = forms.DecimalField(label='Bid Amount', min_value=0.01)
