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

# {% data series "name" %}...{% enddata %}

def _remove_quotes(s):
    if s[0] in ('"', "'") and s[-1] == s[0]:
        return s[1:-1]
    return s

class DataNode(template.Node):
    def __init__(self, nodelist, name, series):
        self._nodelist = nodelist
        self._name = name
        self._series = template.Variable(series)

    def render(self, context):
        '''
        var googlecharts_data_%(name)s = [
            %(data)s
            null // fix trailing comma
        ];
        googlecharts_data_%(name)s.pop();
        googlecharts_data_%(name)s._cl = [%(cl)s];
        '''
        series = self._series.resolve(context)
        nodelist = self._nodelist.get_nodes_by_type(ColNode)
        data = []
        for row in series:
            data.append([node.render(context, row[i]) for i, node in enumerate(nodelist)])
        data_str = ''.join(['[%s],' % ','.join(r) for r in data])
        cl = ','.join(['["%s","%s"]' % (c._typename, c._label) for c in nodelist])
        return self.render.__doc__ % {'name': self._name, 'data': data_str, 'cl': cl}

@register.tag
def data(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError('%r tag requires at least one argument' % args[0])
    while len(args) < 3:
        args.append('default')
    _, series, name = args
    name = _remove_quotes(name)
    nodelist = parser.parse(['enddata'])
    parser.delete_first_token()
    return DataNode(nodelist, name=name, series=series)

# {% col "type" "label" %}...{% endcol %}

class ColNode(template.Node):
    def __init__(self, nodelist, typename, label):
        self._nodelist = nodelist
        self._typename = typename
        self._label = label

    def render(self, context, val):
        context['val'] = val
        return self._nodelist.render(context)

@register.tag
def col(parser, token):
    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError('%r tag requires at least one argument' % args[0])
    while len(args) < 3:
        args.append('')
    _, typename, label = [_remove_quotes(s) for s in args]
    nodelist = parser.parse(['endcol'])
    parser.delete_first_token()
    return ColNode(nodelist, typename=typename, label=label)

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

# {% graph "container" "data" "options" %}

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
