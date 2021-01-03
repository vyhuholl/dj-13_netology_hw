from django import template
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def format_date(created_utc):
    created_utc = datetime.utcfromtimestamp(created_utc)
    delta = datetime.utcnow() - created_utc
    if delta.days == 0:
        if delta.seconds < 600:
            return 'только что'
        return f'{delta.seconds // 3600} часов назад'
    return created_utc.strftime('%Y-%m-%d')


@register.filter
def format_score(score=None):
    if score is not None:
        if score < -5:
            score = 'всё плохо'
        else:
            score = 'хорошо' if score > 5 else 'нейтрально'
    return score


@register.filter
def format_num_comments(num_comments):
    if num_comments == 0:
        return 'Оставьте комментарий'
    elif num_comments > 50:
        return '50+'
    return num_comments


@register.filter
def format_selftext(selftext, count=5):
    tokens = selftext.split()
    if len(tokens) > 2 * count:
        selftext = ' '.join(tokens[:count] + ['...'] + tokens[-count:])
    return selftext
