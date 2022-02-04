from django.shortcuts import render, redirect

def favorites_list(request):
    context = {}
    return render(request, 'favorites_list.html', context=context)

def add_to_favorites(request, id):
    if request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        """
        Get ids list 
        favorites_ids_list = list()
        for item in request.session['favorites']:
            favorites_ids_list.append(item['id'])
            
        check if item exist in list of dicts
        """
        item_exist = next((item for item in request.session['favorites'] if item['type'] == request.POST.get('type') and item['id'] == id), False)
        # print(item_exist)


        #[{}, {}]

        #Get item request data
        add_data = {
            'type': request.POST.get('type'),
            'id': id,
        }

        # if id not in favorites_ids_list:
        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True
    return redirect(request.POST.get('url_from'))


def remove_from_favorites(request, id):
    if request.method == 'POST':
        #delete an item from favorites
        for item in request.session['favorites']:
            if item['id'] == id and item['type'] == request.POST.get('type'):
                item.clear()

        #remove empty {} from favorites
        while {} in request.session['favorites']:
            request.session['favorites'].remove({})


        # remove favorites if favorites
        if not request.session['favorites']:
            del request.session['favorites']
            #request.session.modified = True

        request.session.modified = True
    return redirect(request.POST.get('url_from'))


def delete_favorites(request):
    if request.session.get('favorites'):
        del request.session['favorites']
        # request.session.modified = True
    return redirect(request.POST.get('url_from'))
