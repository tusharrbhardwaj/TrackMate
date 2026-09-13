from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ProofForm(FlaskForm):
    description = TextAreaField(
        "Explanation",
        validators=[
            DataRequired()
        ]
    )
    photo = FileField(
        "Screenshot",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "jpeg", "png"],
                "Only JPG, JPEG and PNG images are allowed."
            )
        ]
    )
    submit = SubmitField("Submit Proof")
