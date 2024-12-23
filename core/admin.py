from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount

# Register the Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_user', 'bio', 'profileimg', 'location')
    search_fields = ('user__username', 'bio', 'location')

# Register the Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'no_of_likes')
    search_fields = ('user', 'caption')
    list_filter = ('created_at',)

# Register the LikePost model
class LikePostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'username')
    search_fields = ('post_id', 'username')

# Register the FollowersCount model
class FollowersCountAdmin(admin.ModelAdmin):
    list_display = ('follower', 'user')
    search_fields = ('follower', 'user')

# Register the models with the admin site
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(LikePost, LikePostAdmin)
admin.site.register(FollowersCount, FollowersCountAdmin)
