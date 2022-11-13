from goods.models import Category


def all_categories_context(request):
    return {'category': Category.objects.all()}
