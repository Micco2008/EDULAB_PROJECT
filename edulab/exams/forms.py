from django import forms
from django.forms import modelformset_factory
from .models import Exam, Question, Answer


class ExamFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        class_choices = kwargs.pop("class_choices", [])
        subject_choices = kwargs.pop("subject_choices", [])
        super().__init__(*args, **kwargs)
        self.fields["school_class"].choices = class_choices
        self.fields["subject"].choices = subject_choices

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-12 pr-4 py-3 '
                     'rounded-lg border border-gray-200'
                     ' focus:ring-2 focus:ring-[#2D3B31]'
                     ' focus:border-[#2D3B31] bg-white',
            'placeholder': 'Поиск тестов...'})

    )

    school_class = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'class': "px-4 py-3 "
                     "rounded-lg "
                     "border border-gray-200 "
                     "focus:ring-2 focus:ring-[#2D3B31] bg-white"})
    )

    subject = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(attrs={
            'class': "px-4 py-3 "
                     "rounded-lg "
                     "border border-gray-200 "
                     "focus:ring-2 focus:ring-[#2D3B31] bg-white"})
    )


class QuestionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        question = kwargs.pop("question", [])
        super().__init__(*args, **kwargs)
        if question.answers.filter(is_correct=True).count() == 1:
            self.fields["answers"] = forms.ModelChoiceField(
                queryset=Exam.objects.all(),
                required=True,
                widget=forms.RadioSelect(
                    attrs={'style': 'padding: 40px;'}
                ),
            )

            self.one_correct = True
        else:
            self.one_correct = False

        self.fields["answers"].queryset = question.answers.all()
        self.fields["answers"].label = question.question

    answers = forms.ModelMultipleChoiceField(
        queryset=Exam.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(
            attrs={'style': 'padding: 40px;'}
        ),
    )


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'subject', 'class_school']


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']


QuestionFormSet = modelformset_factory(
    Question,
    fields=['question'],
    extra=1,
    can_delete=True
)


AnswerFormSet = modelformset_factory(
    Answer,
    fields=['answer', 'is_correct'],
    extra=1,
    can_delete=True
)