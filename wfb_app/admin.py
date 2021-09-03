from django.contrib import admin

from wfb_app.models import GameResults, Armys, Units, Profile, Parings_3, Parings_5


class GameResultsAdmin(admin.ModelAdmin):
    list_display = ("user", "army", "battle_points", "objective", "objective_type", "game_rank", "opponent_dw", "opponent", "opponent_army", "date")
    list_editable = ("army", "battle_points", "objective", "objective_type", "game_rank", "opponent_dw", "opponent", "opponent_army", "date")

class ArmysAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "description")
    list_editable = ("short_name", "description")

class UnitsAdmin(admin.ModelAdmin):
    list_display = ("name", "offensive", "strength", "ap", "reflex", "army")
    list_editable = ("offensive", "strength", "ap", "reflex", "army")

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_army")

class Parings3Admin(admin.ModelAdmin):
    list_display = ("name", "p1", "p2", "p3", "op1", "op2", "op3")

class Parings5Admin(admin.ModelAdmin):
    list_display = ("name", "p1", "p2", "p3", "op1", "op2", "op3")


admin.site.register(GameResults, GameResultsAdmin)
admin.site.register(Armys, ArmysAdmin)
admin.site.register(Units, UnitsAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Parings_3, Parings3Admin)
admin.site.register(Parings_5, Parings5Admin)
