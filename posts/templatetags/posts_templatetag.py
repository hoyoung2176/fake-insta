from django import template

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content + ' '
    hashtags = post.hashtags.all()
    
    # hashtags 를 순회하면서, content 내에서 해당 문자열(해시태그)를 링크를 포함한 문자열로 치환한다.
    for hashtag in hashtags:
        #1
        content = content.replace(hashtag.content+ ' ', f'<a href="/posts/hashtag/{hashtag.pk}/">{ hashtag.content}</a>')
        # content = content.replace(f'{hashtag.content}, "<a href='/posts/hashtag/" + str(hashtag.pk) +"/'>" + hashtag.content + "</a>")
        
        #2
        # content = re.sub(fr'hashtag.content'{})
        # content = re.sub(r'\#' )
    return content