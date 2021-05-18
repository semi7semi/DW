from django.contrib import admin

from wfb_app.models import GameResults, Armys, Units, Profile


class GameResultsAdmin(admin.ModelAdmin):
    list_display = ("user", "army", "battle_points", "objective", "objective_type", "game_rank", "opponent_dw", "opponent", "date")
    list_editable = ("army", "battle_points", "objective", "objective_type", "game_rank", "opponent_dw", "opponent", "date")

class ArmysAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "description")
    list_editable = ("short_name", "description")

class UnitsAdmin(admin.ModelAdmin):
    list_display = ("name", "offensive", "strength", "ap", "reflex", "army")
    list_editable = ("offensive", "strength", "ap", "reflex", "army")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_army")




admin.site.register(GameResults, GameResultsAdmin)
admin.site.register(Armys, ArmysAdmin)
admin.site.register(Units, UnitsAdmin)
admin.site.register(Profile, ProfileAdmin)
