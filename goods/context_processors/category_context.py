from goods.models import SuperCategory


def all_categories_context(request):
    return {'supercategory': SuperCategory.objects.all()}


#def mycompare(request):
#    if not request.session.get("compare"):
#        return {'compare': 0}
#    else:
#        return {'compare': len(request.session.get("compare"))}