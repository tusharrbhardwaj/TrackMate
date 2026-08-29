from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ProofForm(FlaskForm):
    description = TextAreaField(
        "Explanation",
        validators=[
            DataRequired(),
            Length(max=1000)
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