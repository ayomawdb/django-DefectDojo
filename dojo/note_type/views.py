import logging

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from dojo.forms import NoteTypeForm, EditNoteTypeForm
from dojo.models import Note_Type
from dojo.filters import NoteTypesFilter
from dojo.utils import get_page_items, add_breadcrumb

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_superuser)
def note_type(request):
    initial_queryset = Note_Type.objects.all().order_by('name')
    name_words = [note_type.name for note_type in
                  initial_queryset]
    ntl = NoteTypesFilter(request.GET, queryset=initial_queryset)
    nts = get_page_items(request, ntl.qs, 25)
    add_breadcrumb(title="Note Type List", top_level=True, request=request)
    return render(request, 'dojo/note_type.html', {
        'name': 'Note Type List',
        'metric': False,
        'user': request.user,
        'nts': nts,
        'ntl': ntl,
        'name_words': name_words})

@user_passes_test(lambda u: u.is_superuser)
def edit_note_type(request, ntid):
    nt = get_object_or_404(Note_Type, pk=ntid)
    No_of_notes = nt.No_of_notes
    nt_form = EditNoteTypeForm(instance=nt, No_of_notes = No_of_notes)
    if request.method == "POST" and request.POST.get('edit_note_type'):
        nt_form = EditNoteTypeForm(request.POST, instance=nt, No_of_notes = No_of_notes)
        if nt_form.is_valid():
            nt = nt_form.save()
            Handle_other_notetype()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Note type updated successfully.',
                extra_tags="alert-success",
            )
            return HttpResponseRedirect(reverse("note_type"))
    if request.method == "POST" and request.POST.get("disable_note_type"):
            nt.is_active=False
            nt.save()
            Handle_other_notetype()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Note type Disabled successfully.",
                extra_tags="alert-success",
            )
            return HttpResponseRedirect(reverse("note_type"))
    if request.method == "POST" and request.POST.get("re-activate_note_type"):
            nt.is_active=True
            nt.save()
            Handle_other_notetype()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Note type Activated successfully.",
                extra_tags="alert-success",
            )
            return HttpResponseRedirect(reverse("note_type"))
    add_breadcrumb(title="Edit Note Type", top_level=False, request=request)
    return render(request, 'dojo/edit_note_type.html', {
        'name': 'Edit Note Type',
        'metric': False,
        'user': request.user,
        'nt_form': nt_form,
        'nt': nt})

@user_passes_test(lambda u: u.is_superuser)
def add_note_type(request):
    form = NoteTypeForm()
    if request.method == 'POST':
        form = NoteTypeForm(request.POST)
        if form.is_valid():
            note_type = form.save()
            Handle_other_notetype()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Note Type added successfully.',
                                 extra_tags='alert-success')
            return HttpResponseRedirect(reverse('note_type'))
    add_breadcrumb(title="Add Note Type", top_level=False, request=request)
    return render(request,'dojo/add_note_type.html' , {'form' : form})

def Handle_other_notetype():
    mandatory_active_notetypes = Note_Type.objects.filter(is_mandatory=True, is_active=True, Related_to='Finding')
    nt = get_object_or_404(Note_Type, pk=1)
    if nt.is_mandatory == True:
        if len(mandatory_active_notetypes) > 1:
            nt.is_mandatory = False
            nt.save()
    else:
        if len(mandatory_active_notetypes) == 0:
            nt.is_mandatory = True
            nt.save()
