from django.conf.urls import url

from dojo.note_types import views

urlpatterns = [
    url(r'^note_type$',
        views.note_type, name='note_type'),
    url(r'^note/type/(?P<ntid>\d+)/edit$',
        views.edit_note_type, name='edit_note_type'),
    url(r'^add_note_type$',
        views.add_note_type, name='add_note_type'),
    ]
