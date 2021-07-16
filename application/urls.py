from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    path('add-question', views.add_question, name="add-question"),
    path('view-question/<question_id>',
         views.view_question, name="view-question"),


    path('save-question', views.save_question, name="save-question"),

    path('save-question-elements', views.save_question_elements,
         name="save-question-elements"),

    path('save-rule', views.save_rule, name="save-rule"),
    path('save-loop', views.save_loop, name="save-loop"),
    path('complete-question', views.complete_question, name="complete-question"),


    path('save-exercise', views.save_exercise, name="save-exercise")


]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
