from django.contrib import admin
from django.db.models.base import Model
from django.utils import timezone

from .models import QuestionOption, BinaryQuestionOption, ScoreQuestionOption
from .models import Question, BinaryQuestion, ScoreQuestion
from .models import Voting, BinaryVoting, ScoreVoting

from .filters import StartedFilter


def start(modeladmin, request, queryset):
    for v in queryset.all():
        v.create_pubkey()
        v.start_date = timezone.now()
        v.save()


def stop(ModelAdmin, request, queryset):
    for v in queryset.all():
        v.end_date = timezone.now()
        v.save()


def tally(ModelAdmin, request, queryset):
    for v in queryset.filter(end_date__lt=timezone.now()):
        token = request.session.get('auth-token', '')
        v.tally_votes(token)


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption


class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]


class VotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    #date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]

class BinaryQuestionOptionInline(admin.TabularInline):
    model = BinaryQuestionOption

class BinaryQuestionAdmin(admin.ModelAdmin):
    inlines = [BinaryQuestionOptionInline]

class BinaryVotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    #date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]


class ScoreQuestionOptionInline(admin.TabularInline):
    model = ScoreQuestionOption

class ScoreQuestionAdmin(admin.ModelAdmin):
    inlines = [ScoreQuestionOptionInline]

class ScoreVotingAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    readonly_fields = ('start_date', 'end_date', 'pub_key',
                       'tally', 'postproc')
    #date_hierarchy = 'start_date'
    list_filter = (StartedFilter,)
    search_fields = ('name', )

    actions = [ start, stop, tally ]

admin.site.register(Voting, VotingAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(BinaryVoting, BinaryVotingAdmin)
admin.site.register(BinaryQuestion, BinaryQuestionAdmin)
admin.site.register(ScoreVoting, ScoreVotingAdmin)
admin.site.register(ScoreQuestion, ScoreQuestionAdmin)