from flask_wtf import FlaskForm;
from wtforms import (StringField, TextAreaField, DateTimeLocalField, IntegerField, SubmitField);
from wtforms.validators import ( DataRequired, Length, NumberRange);


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
    weight = IntegerField(
        "Weight (%)",
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100)
        ]
    )

    submit = SubmitField("Create Task")