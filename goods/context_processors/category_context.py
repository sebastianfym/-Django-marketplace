from goods.models import Category


def all_categories_context(request):
    return {'category': Category.objects.all()}


def mycompare(request):
    if not request.session.get("compare"):
        return {'compare': 0}
    else:
        return {'compare': len(request.session.get("compare"))}