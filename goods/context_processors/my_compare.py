def mycompare(request):
    if not request.session.get("compare"):
        return {'compare': 0}
    else:
        return {'compare': len(request.session.get("compare"))}