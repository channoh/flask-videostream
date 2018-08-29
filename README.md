# flask-videostream
testing video stream web server with python flask (+gunicorn)

## Command-line Example

```bash
$ gunicorn -w 3 --worker-connections 3 wsgi --timeout 12000 --preload
```
