import urllib, hashlib, datetime
from google.appengine.ext import db

class Gravatar:
    def gravatar(self, size=40):
        gravatar_url = "http://www.gravatar.com/avatar.php?"
        gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(self.email.lower()).hexdigest(), 'size':str(size), 'default':'identicon'})
        return gravatar_url

class GravatarUser(Gravatar):
    def get_email(self):
        try:
            return self.goog.email()
        except Exception:
            return 'nan'

    def get_nickname(self):
        try:
            nick = self.user.nickname()
            if nick.find('@') >= 0:
                return nick[0:nick.index('@')]
            return nick
        except Exception:
            return 'anonymous'

    nickname  = property(get_nickname, None, None, "nickname of user")
    email = property(get_email, None, None, "email of creator")

class NiceDates:
    def pubDate(self):
        return self.created.strftime("%a, %d %b %Y %H:%M:%S GMT")

    def pretty_date(self):
        return self.created.strftime("%a, %d %b %Y")


class Anchor:
    def anchor(self):
        return "%s-%s" % (self.__class__.__name__.lower(), str(self.key())[-8:])


class Forum(db.Model):
    slug        = db.StringProperty()
    name        = db.StringProperty()
    description = db.TextProperty()


class Topic(db.Model, GravatarUser, NiceDates):
    forum = db.Reference(Forum)
    title = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_post = db.DateTimeProperty(auto_now_add=True)
    user = db.UserProperty()


class Post(db.Model, GravatarUser, NiceDates, Anchor):
    topic = db.Reference(Topic)
    user = db.UserProperty()
    body = db.TextProperty()
    body_html = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class Redirect(db.Model):
    slug      = db.StringProperty()
    url       = db.StringProperty()


class Page(db.Model):
    slug            = db.StringProperty()
    title           = db.StringProperty()
    body            = db.TextProperty()
    metaDescription = db.StringProperty()
    created         = db.DateTimeProperty(auto_now_add=True)
    updated         = db.DateTimeProperty()


class PageVersion(db.Model):
    page = db.Reference(Page)
    body = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class Article(db.Model, NiceDates):
    title = db.StringProperty()
    slug = db.StringProperty()
    body = db.TextProperty()
    draft = db.BooleanProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    tags = db.ListProperty(basestring, default=None)

    def previous(self):
        return db.GqlQuery("SELECT * FROM Article WHERE created < :1 ORDER BY created DESC LIMIT 5", self.created)


class Comment(db.Model, Gravatar, NiceDates, Anchor):
    article = db.Reference(Article)
    name = db.StringProperty()
    email = db.StringProperty()
    url = db.StringProperty()
    body = db.TextProperty()
    body_html = db.TextProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    raw = db.TextProperty()

class User(db.Model, GravatarUser):
    name = db.StringProperty()
    goog = db.UserProperty()
    timestamp = db.DateTimeProperty(auto_now=True)

class Extension(db.Model, NiceDates):
    mid = db.StringProperty()
    name = db.StringProperty()
    icon_url = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now=True)
    updateRDF = db.StringProperty()
    description = db.StringProperty()
    creator = db.StringProperty()
    homepageURL = db.StringProperty()
    developers = db.ListProperty(basestring)
    translators = db.ListProperty(basestring)
    contributors = db.ListProperty(basestring)

class Profile(db.Model):
    secret = db.StringProperty()
    name = db.StringProperty()
    os = db.StringProperty()
    version = db.StringProperty()
    user = db.Reference(User)
    platform = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now=True)

class ProfileExtension(db.Model, NiceDates):
    extension = db.Reference(Extension)
    profile = db.Reference(Profile)
    user = db.Reference(User)
    version = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now=True)

class ExtensionRecommendation(db.Model):
    recommended = db.Reference(Extension, collection_name="recommended")
    extension = db.Reference(Extension)
    timestamp = db.DateTimeProperty(auto_now=True)
