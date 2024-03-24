from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),
    path('bots', views.BotsView.as_view(), name='bots'),
    path('delete_bot/<int:bot_id>/', views.delete_bot, name='delete_bot'),
    path('bot_add', views.AddBotView.as_view(), name='add_bot'),
    path('bot_import', views.ImportBotView.as_view(), name='import_bot'),
    re_path(r'^bot/(?P<bot_id>\d+)$', views.EditBotView.as_view(), name='bot_detail'),
    re_path(r'^bot/(?P<bot_id>\d+)/action/edit/(?P<action_id>\d+)$', views.ActionsView.as_view(), name='edit_action'),
    re_path(r'^bot/(?P<bot_id>\d+)/intent/add$', views.AddIntentView.as_view(), name='add_intent'),
    re_path(r'^bot/intent/(?P<intent_id>\d+)$', views.EditIntentView.as_view(), name='edit_intent'),
    re_path(r'^bot/intent/(?P<intent_id>\d+)/expression/add$', views.AddExpressionView.as_view(), name='add_expression'),
    re_path(r'^bot/intent/(?P<intent_id>\d+)/delete_expression/(?P<expression_id>\d+)$', views.delete_expression, name='delete_expression'),
    re_path(r'^bot/intent/(?P<intent_id>\d+)/expression/(?P<expression_id>\d+)/parameter/add$', views.add_parameter, name='add_parameter'),
    re_path(r'^bot/intent/(?P<intent_id>\d+)/parameter/(?P<parameter_id>\d+)/update$', views.update_parameter, name='update_parameter'),
    re_path(r'^bot/intent/(?P<intent_id>\d+)/parameter/(?P<parameter_id>\d+)/delete$', views.delete_parameter, name='delete_parameter'),
    re_path(r'^bot/intent/(?P<intent_id>\d+)/expression/(?P<expression_id>\d+)/predict$', views.predict_expression, name='predict_expression'),
    re_path(r'^bot/(?P<bot_id>\d+)/stories/$', views.StoriesView.as_view(), name='stories'),
    re_path(r'^bot/(?P<bot_id>\d+)/entity/add$', views.AddEntityView.as_view(), name='add_entity'),
    re_path(r'^bot/(?P<bot_id>\d+)/entity/(?P<entity_id>\d+)$', views.EditEntityView.as_view(), name='edit_entity'),
    re_path(r'^bot/(?P<bot_id>\d+)/entity/(?P<entity_id>\d+)/delete$', views.delete_entity, name='delete_entity'),
    re_path(r'^bot/(?P<bot_id>\d+)/regex/add$', views.AddRegexView.as_view(), name='add_regex'),
    re_path(r'^bot/(?P<bot_id>\d+)/regex/(?P<regex_id>\d+)$', views.EditRegexView.as_view(), name='edit_regex'),
    re_path(r'^bot/(?P<bot_id>\d+)/regex/(?P<regex_id>\d+)/delete$', views.delete_regex, name='delete_regex'),
    re_path(r'^bot/(?P<bot_id>\d+)/synonym/(?P<synonym_id>\d+)$', views.EditSynonymView.as_view(), name='edit_synonym'),
    re_path(r'^bot/(?P<bot_id>\d+)/synonym/(?P<synonym_id>\d+)/add_synonym_variant$', views.add_synonym_variant, name='add_synonym_variant'),
    re_path(r'^bot/(?P<bot_id>\d+)/synonym/(?P<synonym_id>\d+)/remove_synonym_variant$', views.remove_synonym_variant, name='remove_synonym_variant'),
    re_path(r'^bot/(?P<bot_id>\d+)/synonyms/add$', views.AddSynonymView.as_view(), name='add_synonym'),
    re_path(r'^bot/(?P<bot_id>\d+)/synonym/delete/(?P<synonym_id>\d+)$', views.delete_synonym, name='delete_synonym'),
    path('rasaconfig', views.RasaConfigView.as_view(), name='rasa_config'),
    path('logs', views.LogsView.as_view(), name='logs'),
    path('history', views.HistoryView.as_view(), name='history'),
    re_path(r'^conversation/(?P<bot_id>\d+)/(?P<user_id>\d+)$', views.ConversationView.as_view(), name='conversation'),
    path('insights', views.InsightsView.as_view(), name='insights'),
    path('training', views.TrainingView.as_view(), name='training'),
    re_path(r'^training/(?P<bot_id>\d+)$', views.TrainingView.as_view(), name='training'),
    path('settings', views.SettingsView.as_view(), name='settings'),
    path('models', views.ModelView.as_view(), name='models'),
    re_path(r'^models/(?P<bot_id>\d+)$', views.ModelView.as_view(), name='models'),
    path('load_model/<str:server_path>/', views.load_model, name='load_model'),
    path('delete_model/<int:model_id>/', views.delete_model, name='delete_model'),
    re_path(r'^models/(?P<bot_id>\d+)/add$', views.AddModelView.as_view(), name='add_model'),
    re_path(r'^chat/(?P<bot_id>\d+)$', views.ChatView.as_view(), name='chat'),
    path('chat', views.ChatView.as_view(), name='chat'),
    path('stories', views.StoriesView.as_view(), name='stories'),
    re_path(r'^stories/(?P<bot_id>\d+)$', views.StoriesView.as_view(), name='stories'),
    re_path(r'^stories/(?P<bot_id>\d+)/search$', views.search_text, name='search_text'),
    re_path(r'^stories/(?P<bot_id>\d+)/add$', views.AddStoryView.as_view(), name='add_story'),
    re_path(r'^stories/(?P<bot_id>\d+)/edit/(?P<story_id>\d+)$', views.EditStoryView.as_view(), name='edit_story'),
    re_path(r'^stories/detail/(?P<story_id>\d+)$', views.StoryDetailView.as_view(), name='story_detail'),
    re_path(r'^stories/(?P<bot_id>\d+)/delete/(?P<story_id>\d+)$', views.delete_story, name='delete_story'),
    re_path(r'^stories/(?P<bot_id>\d+)/save_story_step$', views.save_story_step, name='save_story_step'),
    path('responses', views.ResponseView.as_view(), name='responses'),
    re_path(r'^responses/(?P<bot_id>\d+)$', views.ResponseView.as_view(), name='responses'),
    re_path(r'^responses/(?P<bot_id>\d+)/add$', views.AddActionView.as_view(), name='add_response'),
    re_path(r'^responses/(?P<bot_id>\d+)/delete_action$', views.delete_action, name='delete_action'),
    re_path(r'^responses/(?P<bot_id>\d+)/add_response$', views.add_response, name='add_response'),
    re_path(r'^responses/(?P<bot_id>\d+)/update_response$', views.update_response, name='update_response'),
    re_path(r'^responses/(?P<bot_id>\d+)/delete_response$', views.delete_response, name='delete_response'),
    re_path(r'^responses/(?P<bot_id>\d+)/delete_response/(?P<response_id>\d+)$', views.DeleteResponseView.as_view(), name='delete_response'),
    re_path(r'^responses/(?P<bot_id>\d+)/edit_response/(?P<response_id>\d+)$', views.EditResponseView.as_view(), name='edit_response'),
    path('download_file/', views.download_file, name='download_file'),
]
