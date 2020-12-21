from django.contrib import admin

from wfb_app.models import GameResults, Armys


class GameResultsAdmin(admin.ModelAdmin):
    list_display = ("user", "battle_points", "objective", "objective_type", "game_rank", "opponent", "date")
    list_editable = ("battle_points", "objective", "objective_type", "game_rank", "opponent", "date")

class ArmysAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "description")
    list_editable = ("short_name", "description")


admin.site.register(GameResults, GameResultsAdmin)
admin.site.register(Armys, ArmysAdmin)
