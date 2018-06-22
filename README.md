This is a simple trigger via get request (fill the URL with the proper endpoint 
parameters):
```
<script>
var xhr = new XMLHttpRequest();
xhr.open('GET', "https://***.execute-api.***.amazonaws.com/dev/count", 
true);
xhr.send();
</script>
```
