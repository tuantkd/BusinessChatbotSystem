from django import forms
from .models import Action, Bot, Intent, Response, Story

class BotForm(forms.ModelForm):
    bot_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter bot name here...', 'class': 'form-control'}))
    bot_config = forms.CharField(
        label='Bot Config',
        widget=forms.Textarea(attrs={'placeholder': 'Enter bot config here...', 'class': 'form-control'})
    )
    output_folder = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Folder path...', 'class': 'form-control'}))

    class Meta:
        model = Bot
        fields = ['bot_name', 'bot_config', 'output_folder']

class ImportBotForm(forms.Form):
    bot_name = forms.CharField(label='Bot Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter the bot name', 'class': 'form-control'}))
    file = forms.FileField(label='Bot Configuration File', widget=forms.FileInput(attrs={'accept': '.json', 'class': 'form-control'}))

class ActionForm(forms.ModelForm):
    action_name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the action name'}))
    class Meta:
        model = Action
        fields = ['action_name']

class ResponseForm(forms.ModelForm):
    RESPONSE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]

    response_text = forms.CharField(
        label='Response',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the response text', 'rows': 4}),
    )
    response_type = forms.ChoiceField(
        label='Response Type',
        choices=RESPONSE_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    response_file = forms.FileField(
        label='File',
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=False  # Đặt là không bắt buộc, vì không phải lúc nào cũng cần tải lên tệp
    )

    class Meta:
        model = Response
        fields = ['response_type', 'response_text', 'response_file']

    def clean(self):
        cleaned_data = super().clean()
        response_type = cleaned_data.get('response_type')
        response_text = cleaned_data.get('response_text')
        response_file = cleaned_data.get('response_file')

        # Thêm logic để xác minh dữ liệu dựa trên kiểu phản hồi
        if response_type == 'text' and not response_text:
            self.add_error('response_text', 'This field is required for text responses.')
        elif response_type in ['image', 'video', 'audio'] and not response_file:
            self.add_error('response_file', 'Uploading a file is required for this response type.')

class IntentForm(forms.ModelForm):
    class Meta:
        model = Intent
        fields = ['intent_name']
# forms.py

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['story_name', 'story', 'bot']
        widgets = {
            'story_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter story name'}),
            'story': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter details of the story', 'rows': 4}),
            'bot': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(StoryForm, self).__init__(*args, **kwargs)
        # Optionally, add a bootstrap class to the timestamp field's widget if you want to include it in the form.
        self.fields['timestamp'].widget = forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Select a date and time'})

