# django-mapshader
Placeholder from Django Mapshader Integration

## Installation
```bash
pip install django-mapshader
```

## Configuration

* Add mapshader into INSTALLED_APPS
```python
INSTALLED_APPS - [
  ...
  'django_mapshader'
]
```
* Include the django_mapshader URLconf in your project urls.py like this:
```python
path('mapshader/', include('django_mapshader.urls')),
```

* Visit http://127.0.0.1:8000/mapshader/
