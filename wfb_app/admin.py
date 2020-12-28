from django.contrib import admin

from wfb_app.models import GameResults, Armys, Units


class GameResultsAdmin(admin.ModelAdmin):
    list_display = ("user", "battle_points", "objective", "objective_type", "game_rank", "opponent", "date")
    list_editable = ("battle_points", "objective", "objective_type", "game_rank", "opponent", "date")

class ArmysAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "description")
    list_editable = ("short_name", "description")

class UnitsAdmin(admin.ModelAdmin):
    list_display = ("name", "offensive", "strength", "ap", "reflex", "army")
    list_editable = ("offensive", "strength", "ap", "reflex", "army")


admin.site.register(GameResults, GameResultsAdmin)
admin.site.register(Armys, ArmysAdmin)
admin.site.register(Units, UnitsAdmin)
