from .forms import ContactForm
from .models import Post, Category

class ContactFormMixin(object):

    def get_context_data(self, *args, **kwargs):
        context = super(ContactFormMixin, self).get_context_data(*args, **kwargs)
        context["categories"] = Category.objects.all()
        context["latest_posts"] = Post.objects.all().order_by('-published_date')[:3]
        context["contact"] = ContactForm
        return context
