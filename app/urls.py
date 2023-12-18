from app.alumni.urls import urlpatterns as alumni_urls
from app.analytics.urls import urlpatterns as analytics_urls
from app.authentication.urls import urlpatterns as authentication_urls
from app.chapters.urls import urlpatterns as chapters_urls
from app.events.urls import urlpatterns as events_urls
from app.feedback.urls import urlpatterns as feedback_urls
from app.hubs.urls import urlpatterns as hubs_urls
from app.news.urls import urlpatterns as news_urls
from app.opportunities.urls import urlpatterns as opportunities_urls
from app.user_module.urls import urlpatterns as users_urls
from app.posts.urls import urlpatterns as posts_urls

urlpatterns = (
    authentication_urls
    + users_urls
    + chapters_urls
    + events_urls
    + hubs_urls
    + opportunities_urls
    + feedback_urls
    + news_urls
    + analytics_urls
    + alumni_urls
    + posts_urls
)
