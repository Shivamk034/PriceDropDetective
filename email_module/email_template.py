def get_template_price_drop_email(name,product_name,product_url,previous_price,new_price,product_detail_url):

    prod_name_len = 20
    subject = f""" Price Drop Alert!  | {product_name[:prod_name_len]+("..." if len(product_name)>prod_name_len else "")}"""
    
    with open("email_module/email_template.html","r") as f:
        html = f.read()

    body = html.format(
        name=name,
        product_name=product_name,
        product_url=product_url,
        previous_price=previous_price,
        new_price=new_price,
        product_detail_url=product_detail_url,
    )

    return {
        "subject":subject,
        "body":body,
    }


# template = get_template_price_drop_email(name,product_name,product_url,previous_price,new_price,product_detail_url)
