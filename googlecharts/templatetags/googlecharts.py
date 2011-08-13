from django import template
from django.conf import settings

register = template.Library()

# {% googlecharts %}...{% endgooglecharts %}

_api = getattr(settings, 'GOOGLECHARTS_API', '1.1')

class GooglechartsNode(template.Node):
    def __init__(self, nodelist):
        self._nodelist = nodelist

    def render_template(self, template, **kwargs):
        from django.template.loader import render_to_string
        return render_to_string(template, kwargs)

    def render(self, context):
        js = self._nodelist.render(context)
        return self.render_template('googlecharts/googlecharts.html', googlecharts_js=js, api=_api)

@register.tag
def googlecharts(parser, token):
    nodelist = parser.parse(['endgooglecharts'])
    parser.delete_first_token()
    return GooglechartsNode(nodelist)

# {% data "name" %}...{% enddata %}

def _remove_quotes(s):
    if s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s

class DataNode(template.Node):
    def __init__(self, nodelist, name):
        self._nodelist = nodelist
        self._name = name

    def render(self, context):
        '''
        var googlecharts_data_%(name)s = [
            %(data)s
            null // fix trailing comma
        ];
        googlecharts_data_%(name)s.pop();
        '''
        return self.render.__doc__ % {'name': self._name, 'data': self._nodelist.render(context)}

@register.tag
def data(parser, token):
    try:
        _, name = token.split_contents()
        name = _remove_quotes(name)
    except ValueError:
        name = 'default'
    nodelist = parser.parse(['enddata'])
    parser.delete_first_token()
    return DataNode(nodelist, name=name)

# {% options "name" %}...{% endoptions %}

class OptionsNode(template.Node):
    def __init__(self, nodelist, name):
        self._nodelist = nodelist
        self._name = name

    def render(self, context):
        '''
        var googlecharts_options_%(name)s = {
            %(data)s
        };
        '''
        return self.render.__doc__ % {'name': self._name, 'data': self._nodelist.render(context)}

@register.tag
def options(parser, token):
    try:
        _, name = token.split_contents()
        name = _remove_quotes(name)
    except ValueError:
        name = 'default'
    nodelist = parser.parse(['endoptions'])
    parser.delete_first_token()
    return OptionsNode(nodelist, name=name)

# {% chart "container" "data" "options" %}

class GraphNode(template.Node):
    def __init__(self, **kwargs):
        self._args = kwargs

    def render(self, context):
        '''
        opt = _clone(googlecharts_options_%(options)s);
        opt.container = "%(container)s";
        opt.rows = googlecharts_data_%(data)s;
        googlecharts.push(opt);
        '''
        return self.render.__doc__ % self._args

@register.tag
def graph(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError('%r tag requires at least one argument' % args[0])
    while len(args) < 4:
        args.append('default')
    _, container, data, options = [_remove_quotes(s) for s in args]
    return GraphNode(container=container, data=data, options=options)
