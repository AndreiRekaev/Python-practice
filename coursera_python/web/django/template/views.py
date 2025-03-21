from django.shortcuts import render

def echo(request):
    context = {
        "GET": request.GET,
        "POST": request.POST,
        "statement": request.META.get("HTTP_X_PRINT_STATEMENT", "empty"),
        "META": request.META
    }
    return render(request, 'echo.html', context=context)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
