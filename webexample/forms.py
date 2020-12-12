from django import forms
from .models import Measurement


class MeasurementModelForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ('location', 'destination', 'cafes', 'bars', 'fast_food', 'pharmacy', 'fountain', 'bicycle_rental',
        'ice_cream', 'clock', 'bureau_de_change', 'historic', 'supermamrket', 'clothes', 'bakery', 'beauty', 'kiosk', 'florist')
