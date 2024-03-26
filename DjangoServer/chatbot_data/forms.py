from django import forms
from .models import Action, Bot, Entity, Intent, LookupVariant, Regex, Response, Rule, Story, Synonym, SynonymVariant, Lookup

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
class RegexForm(forms.ModelForm):
    class Meta:
        model = Regex
        fields = ['regex_name']
        widgets = {
            'regex_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter regex name'}),
        }
        
class ImportBotForm(forms.Form):
    file = forms.FileField(label='Bot Configuration File', widget=forms.FileInput(attrs={'accept': '.yml', 'class': 'form-control'}))
class ActionForm(forms.ModelForm):
    ACTION_TYPE_CHOICES = [
        ('utter', 'Utter'),
        ('action', 'Action'),
        ('form', 'Form'),
        ('slot_set', 'Slot Set'),
    ]

    action_name = forms.CharField(label='Name', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the action name'}))
    action_type = forms.ChoiceField(label='Type', choices=ACTION_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    action_config = forms.CharField(label='Config', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the action config'}))
    class Meta:
        model = Action
        fields = ['action_name', 'action_type', 'action_config']


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
            
class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = ['rule_name']
        widgets = {
            'rule_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter rule name'}),
        }
class IntentForm(forms.ModelForm):
    class Meta:
        model = Intent
        fields = ['intent_name']
# forms.py
class SynonymForm(forms.ModelForm):
    class Meta:
        model = Synonym
        fields = ['synonym_reference']
        widgets = {
            'synonym_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter synonym reference'}),
        }
class SynonymVariantForm(forms.ModelForm):
    class Meta:
        model = SynonymVariant
        fields = ['synonym_value']
        widgets = {
            'synonym_value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter synonym variant'}),
        }

class LookupForm(forms.ModelForm):
    class Meta:
        model = Lookup
        fields = ['lookup_name']
        widgets = {
            'lookup_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lookup name'}),
        }

class LookupVariantForm(forms.ModelForm):
    class Meta:
        model = LookupVariant
        fields = ['value']
        widgets = {
            'value': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter lookup variant'}),
        }
class EntityForm(forms.ModelForm):

    class Meta:
        model = Entity
        fields = ['entity_name', 'slot_data_type']
        widgets = {
            'entity_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter entity name'}),
            'slot_data_type': forms.Select(attrs={'class': 'form-control'}),
        }
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['story_name']
        widgets = {
            'story_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter story name'}),
        }

