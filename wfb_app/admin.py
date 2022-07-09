from django.contrib import admin

from wfb_app.models import GameResults, Armys, Units, Profile, Team_of_3, Team_of_4, Team_of_5


class GameResultsAdmin(admin.ModelAdmin):
    list_display = ("user", "army", "battle_points", "objective", "objective_type", "game_rank", "opponent_dw", "opponent", "opponent_army", "date")
    list_editable = ("army", "battle_points", "objective", "objective_type", "game_rank", "opponent_dw", "opponent", "opponent_army", "date")

class ArmysAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "description", "icon")
    list_editable = ("short_name", "description", "icon")

class UnitsAdmin(admin.ModelAdmin):
    list_display = ("name", "offensive", "strength", "ap", "reflex", "army")
    list_editable = ("offensive", "strength", "ap", "reflex", "army")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_army")

class Parings3Admin(admin.ModelAdmin):
    list_display = ("tournament", "name", "op1", "op2", "op3")

class Parings4Admin(admin.ModelAdmin):
    list_display = ("name", "op1", "op2", "op3", "op4")

class Parings5Admin(admin.ModelAdmin):
    list_display = ("name", "op1", "op2", "op3", "op4", "op5")



admin.site.register(GameResults, GameResultsAdmin)
admin.site.register(Armys, ArmysAdmin)
admin.site.register(Units, UnitsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Team_of_3, Parings3Admin)
admin.site.register(Team_of_4, Parings3Admin)
admin.site.register(Team_of_5, Parings3Admin)
