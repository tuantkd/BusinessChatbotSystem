from datetime import datetime, timezone
import pdb
import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.views import View
from django.views.generic.base import TemplateView
from .models import Bot, Action, Response, Story, ModelModel, Conversation
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BotForm, ImportBotForm, ActionForm, ResponseForm, StoryForm
from django.shortcuts import redirect
from django.contrib import messages
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
class BotsView(TemplateView):
    template_name = 'bots/bots.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['botList'] = Bot.objects.all()  # Get all bots
        return context

class EditBotView(View):
    form_class = BotForm
    template_name = 'bots/edit_bot.html'

    def get(self, request, bot_id, *args, **kwargs):
        # Lấy đối tượng bot dựa trên bot_id, nếu không tồn tại thì trả về 404
        bot = get_object_or_404(Bot, pk=bot_id)
        # Khởi tạo form với instance là đối tượng bot
        form = self.form_class(instance=bot)
        # Render template kèm theo form
        return render(request, self.template_name, {'form': form, 'bot': bot})

    def post(self, request, bot_id, *args, **kwargs):
        # Lấy lại đối tượng bot như ở phương thức GET
        bot = get_object_or_404(Bot, pk=bot_id)
        # Khởi tạo form với dữ liệu POST và instance là bot cần cập nhật
        form = self.form_class(request.POST, instance=bot)
        if form.is_valid():
            # Lưu thay đổi vào cơ sở dữ liệu
            form.save()
            # Chuyển hướng người dùng tới trang danh sách bot hoặc trang chi tiết của bot vừa cập nhật
            # Giả sử bạn có một view tên là 'bot_detail' để hiển thị chi tiết bot
            return redirect('bots')
        
        # If the form is not valid, re-render the page with existing form data
        return render(request, self.template_name, {'form': form})


class AddBotView(View):
    form_class = BotForm
    template_name = 'bots/add_bot.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a new URL, assuming you have a view named 'bots'
            # that lists all bots or shows a success page
            return redirect('bots')
        
        # If the form is not valid, re-render the page with existing form data
        return render(request, self.template_name, {'form': form})


class ImportBotView(View):
    form_class = ImportBotForm
    template_name = 'bots/import_bot.html'  # Đường dẫn đến template của bạn

    def get(self, request, *args, **kwargs):
        form = self.form_class()  # Khởi tạo form rỗng
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            # Xử lý file được upload và thông tin khác từ form
            bot_name = form.cleaned_data['bot_name']
            bot_file = request.FILES['file']
            
            # Ở đây, bạn sẽ cần xử lý việc lưu bot vào database
            # hoặc thực hiện các thao tác khác tùy theo logic ứng dụng của bạn
            # Ví dụ:
            # new_bot = BotModel(name=bot_name, config=...)
            # new_bot.save()
            
            # Sau khi xử lý xong, redirect tới trang hoặc thông báo thành công
            return redirect('some_view')  # thay 'some_view' bằng tên của URL/view bạn muốn redirect đến
            
        # Nếu form không hợp lệ, hiển thị lại form với thông báo lỗi
        return render(request, self.template_name, {'form': form})
    
class ActionsView(TemplateView):
    # Assuming there might be a specific template for actions that hasn't been listed
    template_name = 'actions/edit_action.html'  # Adjust if there's an actual path

class AddIntentView(TemplateView):
    template_name = 'intents/add_intent.html'

class EditIntentView(TemplateView):
    template_name = 'intents/edit_intent.html'

class StoriesView(View):
    template_name = 'stories/stories.html'

    def get(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        stories = Story.objects.filter(bot_id=bot_id) if bot_id else []
        bots = Bot.objects.all()
        selected_bot = Bot.objects.get(pk=bot_id) if bot_id else None
        return render(request, self.template_name, {'storyList': stories, 'botList': bots, 'selected_bot': selected_bot})

    def post(self, request, *args, **kwargs):
        # This method would be used if you're creating a story via a form submission
        form = StoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('stories_view')
        return render(request, self.template_name, {'form': form})
    
class AddStoryView(View):
    template_name = 'stories/add_story.html'

    def get(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        new_story = Story()
        timestamp = int(time.mktime(datetime.now().timetuple()))
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        # if not bot return 404

        new_story.bot = selected_bot
        new_story.story_name = "story_" + str(timestamp)
        new_story.timestamp = datetime.now()
        new_story.save()
        return redirect('stories', {'selected_bot': selected_bot}, bot_id=bot_id)

class StoryDetailView(View):
    template_name = 'stories/story_detail.html'

    def get(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        return render(request, self.template_name, {'story': story})

class DeleteStoryView(View):

    def post(self, request, story_id, *args, **kwargs):
        story = get_object_or_404(Story, pk=story_id)
        story.delete()
        return redirect('stories_view')

class EntitiesView(TemplateView):
    # Assuming entities list view might be missing, using 'entities.html' if exists
    template_name = 'entities/entities.html'  # Adjust if there's an actual path

class AddEntityView(TemplateView):
    template_name = 'entities/add_entity.html'

class EditEntityView(TemplateView):
    template_name = 'entities/edit_entity.html'

class AddRegexView(TemplateView):
    template_name = 'regex/add_regex.html'

class EditRegexView(TemplateView):
    template_name = 'regex/edit_regex.html'

class AddSynonymView(TemplateView):
    template_name = 'synonyms/add_synonym.html'

class EditSynonymView(TemplateView):
    template_name = 'synonyms/edit_synonym.html'

class RasaConfigView(TemplateView):
    template_name = 'rasaconfig/rasa_config.html'

class LogsView(TemplateView):
    template_name = 'logs/logs.html'

class HistoryView(TemplateView):
    # Assuming there might be a specific template for history that hasn't been listed
    template_name = 'history/history.html'  # Adjust if there's an actual path

class ConversationView(TemplateView):
    # Assuming conversation view might need a specific template
    template_name = 'conversation/conversation.html'  # Adjust if there's an actual path

class InsightsView(TemplateView):
    template_name = 'insights/insights.html'

class TrainingView(View):
    template_name = 'training/training.html'

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        bot_id = self.kwargs.get('bot_id')
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        context = {
            'botList': bots,
            'selected_bot': selected_bot,
        }
        return render(request, self.template_name, context)


def download_file(request):
    # replace 'filepath' with the actual path to the file you want to serve
    filepath = '/path/to/your/file'
    return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='your_filename')
class SettingsView(TemplateView):
    template_name = 'settings/settings.html'

class ModelView(View):
    template_name = 'models/models.html'

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        bot_id = self.kwargs.get('bot_id')
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        context = {
            'botList': bots,
            'selectedBot': selected_bot,
        }
        return render(request, self.template_name, context)

def load_model(request, server_path):
    # replace with your actual logic for loading a model
    model = ModelModel.objects.get(server_path=server_path)
    model.load()  # assuming you have a method to load the model
    messages.success(request, 'Model loaded successfully.')
    return redirect('models')  # replace with the name of your models page

def delete_model(request, model_id):
    # replace with your actual logic for deleting a model
    model = ModelModel.objects.get(id=model_id)
    model.delete()
    messages.success(request, 'Model deleted successfully.')
    return redirect('models')  # replace with the name of your models page
class AddModelView(TemplateView):
    # Assuming add model view might need a specific template
    template_name = 'models/add_model.html'  # Adjust if there's an actual path

class ResponseView(TemplateView):
    template_name = 'responses/responses.html'

    def get_context_data(self, **kwargs):
        context = super(ResponseView, self).get_context_data(**kwargs)
        bots = Bot.objects.all()
        context['bots'] = bots

        selected_bot_id = self.kwargs.get('bot_id')
        
        if selected_bot_id:
            selected_bot = get_object_or_404(Bot, pk=selected_bot_id)
            actions = Action.objects.filter(bot=selected_bot)
            responses = Response.objects.filter(action__bot=selected_bot)
        else:
            actions = Action.objects.none()  # Tránh lỗi khi không có bot nào được chọn
            responses = Response.objects.none()
    
        context['selected_bot'] = selected_bot_id
        context['actions'] = actions
        context['responses'] = responses
        return context

class AddActionView(View):
    form_class = ActionForm
    template_name = 'responses/add_action.html'

    def get(self, request, *args, **kwargs):
        bot_id = kwargs.get('bot_id')  # Giả sử bot_id được truyền qua URL
        form = self.form_class(initial={'bot': bot_id})
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        bot_id = kwargs.get('bot_id')  # Giả sử bot_id được truyền qua URL
        if form.is_valid():
            new_action = form.save(commit=False)
            new_action.bot_id = bot_id  # Đặt bot_id cho action mới
            new_action.save()
            return HttpResponseRedirect(reverse('responses', kwargs={'bot_id': bot_id}))
        else:
            return render(request, self.template_name, {'form': form, 'bot_id': bot_id})

class ChatView(TemplateView):
    template_name = 'chat/chat.html'  # Điều chỉnh nếu có đường dẫn thực tế

    def get(self, request, *args, **kwargs):
        bots = Bot.objects.all()
        bot_id = self.kwargs.get('bot_id')
        selected_bot = get_object_or_404(Bot, pk=bot_id) if bot_id else None
        conversations = Conversation.objects.filter(bot=selected_bot)
        context = {
            'botList': bots,
            'bot': selected_bot,
            'conversations': conversations
        }
        # Thêm logic của bạn ở đây
        return render(request, self.template_name, context)
    
class DeleteActionView(View):
    def post(self, request, *args, **kwargs):
        bot_id = kwargs.get('bot_id')
        action_id = kwargs.get('action_id')
        
        # Tìm và xóa action nếu nó tồn tại
        action = get_object_or_404(Action, id=action_id, bot_id=bot_id)
        action.delete()
        
        # Redirect người dùng về trang danh sách các response của bot sau khi xóa
        # Đảm bảo bạn đã định nghĩa 'responses_for_bot' URL pattern trong urls.py
        return redirect('responses', bot_id=bot_id)


class AddResponseToActionView(View):
    form_class = ResponseForm
    template_name = 'responses/add_response.html'
    def get(self, request, bot_id, action_id):
        form = self.form_class()
        return render(request, self.template_name , {'form': form, 'bot_id': bot_id, 'action_id': action_id})

    def post(self, request, bot_id, action_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.action = Action.objects.get(id=action_id)  # Ensure this action exists and you handle potential DoesNotExist exception
            response.save()
            return redirect('responses', bot_id=bot_id)  # Replace 'responses_for_bot' with the actual name of your view that lists responses for a bot
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id, 'action_id': action_id})

class DeleteResponseView(View):
    def get(self, request, *args, **kwargs):
        bot_id = kwargs.get('bot_id')
        response_id = kwargs.get('response_id')
        
        # Tìm và xóa response nếu nó tồn tại
        response = get_object_or_404(Response, id=response_id, action__bot_id=bot_id)
        response.delete()
        
        # Redirect người dùng về trang danh sách các response của bot sau khi xóa
        # Đảm bảo bạn đã định nghĩa 'responses_for_bot' URL pattern trong urls.py
        return redirect('responses', bot_id=bot_id)


class EditResponseView(View):
    form_class = ResponseForm
    template_name = 'responses/edit_response.html'

    def get(self, request, bot_id, response_id):
        response = get_object_or_404(Response, id=response_id, action__bot_id=bot_id)
        form = self.form_class(instance=response)
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id, 'response_id': response_id})

    def post(self, request, bot_id, response_id):
        response = get_object_or_404(Response, id=response_id, action__bot_id=bot_id)
        form = self.form_class(request.POST, instance=response)
        if form.is_valid():
            form.save()
            return redirect('responses', bot_id=bot_id)
        return render(request, self.template_name, {'form': form, 'bot_id': bot_id, 'response_id': response_id})