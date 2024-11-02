import urllib.parse

def generate_share_links(recipe_name, recipe_id, base_url):
    encoded_name = urllib.parse.quote(recipe_name)
    recipe_url = f"{base_url}/recipe/{recipe_id}"
    encoded_url = urllib.parse.quote(recipe_url)

    whatsapp_link = f"https://api.whatsapp.com/send?text={encoded_name}%20-%20{encoded_url}"
    facebook_link = f"https://www.facebook.com/sharer/sharer.php?u={encoded_url}"
    twitter_link = f"https://twitter.com/intent/tweet?text={encoded_name}&url={encoded_url}"
    instagram_link = f"https://www.instagram.com/share?url={encoded_url}"  # Note: Instagram doesn't have a direct share URL, this is a placeholder

    return {
        "whatsapp": whatsapp_link,
        "facebook": facebook_link,
        "twitter": twitter_link,
        "instagram": instagram_link
    }