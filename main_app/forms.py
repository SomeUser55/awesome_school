
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField, SelectField, TextAreaField, FieldList, HiddenField

from main_app.models import User, Contest, Role


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    second_name = StringField('Second Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    role = SelectField('Role', choices=Role.ROLES_PUBLIC)

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class CreateContestForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired()])
    unit_test = TextAreaField('Unit Test', validators=[DataRequired()])
    lang = SelectField('Language', choices=Contest.LANGS)
    submit = SubmitField('Save')


class SolveContestForm(FlaskForm):
    code = TextAreaField('Code', validators=[DataRequired()])
    submit = SubmitField('Run')


class CreateBlockForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desc = TextAreaField('Description', validators=[DataRequired()])
    # contest_ids = FieldList(StringField('contest_id'), min_entries=2)
    contest_ids = HiddenField()
    submit = SubmitField('Save', id='submit_button')


class DeleteContestsForm(FlaskForm):
    contest_ids = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Delete', id='submit_button')


class DeleteBlocksForm(FlaskForm):
    block_ids = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Delete', id='submit_button')
