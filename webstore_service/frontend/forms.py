from django import forms
from wtforms.form import Form
from wtforms.fields import StringField, FloatField, SubmitField, TextAreaField, FileField
from wtforms.validators import InputRequired, Length, Optional, ValidationError

class SearchForm(forms.Form):
    search = forms.CharField(max_length=20, required=False)

class NewProduct(Form):
    name = StringField("Title", validators=[InputRequired(), Length(max=50)])
    description = TextAreaField("Description", validators=[InputRequired(), Optional()])
    code = StringField("Code", validators=[InputRequired(), Length(max=20)])
    price = FloatField(label="Price", validators=[InputRequired()])
    image = FileField("Image")
    submit = SubmitField("Add Product")
    