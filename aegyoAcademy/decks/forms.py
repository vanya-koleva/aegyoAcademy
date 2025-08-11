from django import forms
from django.core.exceptions import ValidationError

from decks.choices import CardDifficultyChoices
from decks.models import Deck, Tag, Flashcard


class DeckBaseForm(forms.ModelForm):
    new_tags = forms.CharField(
        label="Add new tags",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Comma-separated new tags',
            'class': 'js-new-tags'
        })
    )

    class Meta:
        model = Deck
        fields = ['title', 'tags', 'is_public']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'js-select-tags'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)

        new_tags = self.cleaned_data['new_tags']

        if commit:
            instance.save()
            self.save_m2m()

        if new_tags:
            for tag_name in new_tags.split(','):
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)

        return instance


class BaseFlashcardForm(forms.ModelForm):
    difficulty = forms.ChoiceField(
        choices=CardDifficultyChoices.choices,
        widget=forms.RadioSelect,
        initial='M'
    )

    class Meta:
        model = Flashcard
        fields = ['question', 'answer', 'difficulty']
        widgets = {
            'question': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter question text...'
            }),
            'answer': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Enter answer text...'
            }),
        }
        labels = {
            'question': 'Question',
            'answer': 'Answer',
        }

    def __init__(self, *args, **kwargs):
        self.deck = kwargs.pop('deck', None)
        super().__init__(*args, **kwargs)

    def clean_question(self):
        question = self.cleaned_data['question'].strip()
        if len(question) < 1:
            raise forms.ValidationError("Question must be at least 1 character long")
        return question

    def clean_answer(self):
        answer = self.cleaned_data['answer'].strip()
        if len(answer) < 1:
            raise forms.ValidationError("Answer must be at least 1 characters long")
        return answer


class SearchForm(forms.Form):
    query = forms.CharField(
        label='',
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'Search for decks...'},
        )
    )


class DeckCreateForm(DeckBaseForm):
    ...


class DeckEditForm(DeckBaseForm):
    ...


class FlashcardCreateForm(BaseFlashcardForm):
    ...


class FlashcardEditForm(BaseFlashcardForm):
    ...