django-google-charts
---

Google Visualization API template tags and helpers for Django framework.

### Dependencies ###

(Not strictly required.)

- `django-qsstats-magic`
- `python-dateutil`

### Installation ###

	$ pip install django-google-charts
	# or
	$ easy_install django-google-charts

Add `'googlecharts'` to your `INSTALLED_APPS`. Optionally, you can specify the
Google Visualization API version: `GOOGLECHARTS_API = '1.1'`, as documented
[here](http://code.google.com/apis/chart/interactive/docs/release_notes.html#ReleaseProcess).

### Basic usage ###

	{% load googlecharts %}
	{# container #}
	<div id="out"></div>
	{% googlecharts %}
		{# named data and options can be reused #}
		{% data values "out_data" %}
			{% col "string" "Name" %}"{{ val }}"{% endcol %}
			{% col "number" "Value" %}{{ val }}{% endcol %}
		{% enddata %}
		{# you can also use global javascript variables here, #}
		{# and call functions #}
		{% options "out_options" %}
			kind: "PieChart",
			options: {
				width: 300,
				height: 240
			}
		{% endoptions %}
		{# chart is assembled from container, data and options #}
		{% graph "out" "out_data" "out_options" %}
	{% endgooglecharts %}

Given the context:

	{'values': [['foo', 32], ['bar', 64], ['baz', 96]]}

The end result looks like this:

![django-google-charts](https://s3.amazonaws.com/files_desu/django-google-charts-basic.png)

See the [source code](https://github.com/mvasilkov/django-google-charts) for more examples.

Google Chart Tools documentation is [here](http://code.google.com/apis/chart/).
