from django.contrib import admin
from django import forms
from .models import Subject, Exam, Question, Answer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2
    fields = ('answer', 'is_correct')

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'answer':
            kwargs['widget'] = forms.TextInput(
                attrs={'size': '40'})
        return super().formfield_for_dbfield(db_field, **kwargs)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    inlines = [AnswerInline]
    fields = ('question',)
    readonly_fields = ('question',)


class ExamForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Exam
        fields = ('name', 'subject', 'class_school', 'questions')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    form = ExamForm
    list_display = ('name', 'subject', 'class_school')
    search_fields = ('name', 'subject__name', 'class_school')
    list_filter = ('subject', 'class_school')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'exam')
    search_fields = ('question', 'exam__name')
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'is_correct')
    search_fields = ('answer', 'question__question')
    list_filter = ('is_correct',)