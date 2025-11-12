def filter_by_price(filter_type : str,products = None):
    if filter_type == 'expensive':
        products = products.order_by('-price')
        
    elif filter_type == 'cheap':
        products = products.order_by('price')
    
    else:
        products = products.all()

    return products