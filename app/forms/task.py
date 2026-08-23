from flask_wtf import FlaskForm;
from wtforms import StringField, TextAreaField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Length


class TaskForm(FlaskForm):
    title = StringField(
        "Task Title",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )
    description = TextAreaField(
        "Description",
        validators=[
            Length(max=500)
        ]
    )
    deadline = DateTimeLocalField(
        "Deadline",
        format="%Y-%m-%dT%H:%M",
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField("Create Task")