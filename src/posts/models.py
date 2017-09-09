from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone
import datetime
from markdown_deux import markdown
from django.utils.safestring import mark_safe
class PostManager(models.Manager):		#override objects.all()
	def active(self, *args, **kwargs):
		# Post.objects.all() == super(PostManager, self).all()
		return super(PostManager, self).filter(draft = False).filter(publish__lte = timezone.now().date())
#super is  orignal call

def upload_location(instance, filename):
	return "%s/%s" %(instance.title, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug =  models.SlugField(null=True, default=None, unique=True)
	image = models.ImageField(
				upload_to = upload_location,
				null = True, 
				blank = True,
	 			height_field = "height_field", 
	 			width_field = "width_field",
	 			max_length = 200,
	 		)
	height_field = models.IntegerField(default = 0)
	width_field = models.IntegerField(default = 0)
	draft = models.BooleanField(default = False)
	publish = models.DateField(default=datetime.date.today, auto_now=False, auto_now_add = False)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add = False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add = True)
	
	objects = PostManager()

	def _str_(self):
		return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug":self.slug})
	def get_absolute_url_update(self):
		return reverse("posts:update", kwargs={"slug":self.slug})
	def get_absolute_url_delete(self):
		return reverse("posts:delete", kwargs={"slug":self.slug})
	
	def get_markdown(self):
		content = self.content
		return mark_safe(markdown(content));
		

def create_slug(instance, new_slug = None):
	
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug = slug).order_by("-id")
	exists = qs.exists()
	if exists:		
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug = new_slug)
	return slug

def pre_save_post_receiver(sender, instance, *args, **keyargs):
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender = Post)