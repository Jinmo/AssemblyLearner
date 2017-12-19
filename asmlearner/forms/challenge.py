from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class ChallengeForm(FlaskForm):
    name = StringField('prob_name', validators=[DataRequired()], description='Name')
    instruction = TextAreaField('prob_instruction', validators=[DataRequired()], description='Instruction')
    suffix = TextAreaField('prob_suffix', validators=[DataRequired()], description='Suffix')
    example = TextAreaField('prob_example', validators=[DataRequired()], description='Example')
    answer_regex = TextAreaField('prob_answer', validators=[DataRequired()], description='Answer')
    category = StringField('category', validators=[DataRequired()], description='Category')
    input = TextAreaField('prob_input', validators=[DataRequired()], description='Input')
    hint = TextAreaField('prob_hint', validators=[DataRequired()], description='Hint')
