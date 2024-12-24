from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, CreateView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse_lazy

from exams.models import Exam, Subject, Question, Answer
from exams.forms import ExamFilterForm, QuestionForm, ExamForm, QuestionFormSet, AnswerFormSet
from exams.serializers import ExamSerializer

class HomePageView(ListView):
    template_name = 'exams/homepage.html'
    context_object_name = 'exams'

    def get_queryset(self):
        subjects = Subject.objects.all()

        self.form = ExamFilterForm(
            self.request.GET or None,
            class_choices=[(0, 'Все классы')] + [(i, f'{i} класс') for i in range(1, 12)],
            subject_choices=[(0, 'Все предметы')] + [(subj.id, subj.name) for subj in subjects],
        )

        if self.form.is_valid():
            search = self.form.cleaned_data['search']
            class_number = int(self.form.cleaned_data['school_class'])
            subject = int(self.form.cleaned_data['subject'])
            query_set = Exam.objects.all()

            if class_number:
                query_set = query_set.filter(class_school=class_number)

            if subject:
                query_set = query_set.filter(subject=Subject.objects.get(id=subject))

            if search:
                query_set = query_set.filter(name__icontains=search)

        else:
            query_set = Exam.objects.all()

        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context


class ExamSolutionView(TemplateView):
    template_name = 'exams/solution.html'
    result_template_name = 'exams/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exam_id = self.kwargs['exam_id']
        exam = get_object_or_404(Exam, pk=exam_id)
        forms = []

        for question in exam.questions.all().order_by('id'):
            forms.append(QuestionForm(question=question, prefix=question.id))

        context['forms'] = forms
        return context


    def post(self, request, *args, **kwargs):
        exam_id = self.kwargs['exam_id']
        exam = get_object_or_404(Exam, pk=exam_id)
        score = max_score = 0

        for question in exam.questions.all().order_by('id'):
            form = QuestionForm(request.POST, question=question, prefix=question.id)

            if form.is_valid():
                if form.one_correct:
                    correct_answer = question.answers.get(is_correct=True)
                    answer = form.cleaned_data['answers']
                    score = score + 1 if correct_answer == answer else score
                else:
                    correct_answers = list(question.answers.filter(is_correct=True).order_by('id'))
                    answers = list(form.cleaned_data['answers'].order_by('id'))
                    score = score + 1 if correct_answers == answers else score
                max_score += 1

        context = super().get_context_data(**kwargs)
        context['percent'] = round(score / max_score * 100 if max_score != 0 else 0, 0)
        context['max_score'] = max_score
        context['score'] = score

        return render(request, self.result_template_name, context)


class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/creation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            question_formset = QuestionFormSet(self.request.POST)
        else:
            question_formset = QuestionFormSet(
                queryset=Question.objects.none())

        context['question_formset'] = question_formset
        return context

    def form_valid(self, form):
        exam = form.save()

        question_formset = QuestionFormSet(self.request.POST)
        if question_formset.is_valid():
            questions = question_formset.save(commit=False)
            for question in questions:
                question.exam = exam
                question.save()

                answer_formset = AnswerFormSet(self.request.POST,
                                               instance=question)
                if answer_formset.is_valid():
                    answers = answer_formset.save(commit=False)
                    for answer in answers:
                        answer.question = question
                        answer.save()

        return redirect(reverse_lazy(
            'exam_list'))

class GetSubjectsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response([subject.name for subject in  Subject.objects.all()], status=status.HTTP_200_OK)


class CreateExamAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ExamSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)