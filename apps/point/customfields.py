import re
from django.db import models
from django.forms import fields
from django.forms import ValidationError
from django.utils.encoding import smart_unicode


class HexColorField(models.CharField):
    
    default_error_messages = {
        'hex_error': u'This is an invalid color code. It must be a html hex color code e.g. 000000FF'
    }

    def clean(self, value, model_instance):
        
        super(HexColorField, self).clean(value, model_instance)
        
        if value in fields.EMPTY_VALUES:
            return u''
        
        value = smart_unicode(value)
        value_length = len(value)
        
        if value_length != 8 or not re.match('^([a-fA-F0-9]{8})$', value):
            raise ValidationError(self.error_messages['hex_error'])
        
        return value

    def widget_attrs(self, widget):
        if isinstance(widget, (fields.TextInput)):
            return {'maxlength': str(8)}

