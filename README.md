
You'll need 'serverless-finch' plugin to deploy static web page to S3 and make
sure to change endpoint URL in client/dist/index.html before deploying to S3
via 'serverless client deploy' 

This is the simple trigger via get request where URL should be changed to
actual endpoint given during 'serverless deploy':
```
<script>
var xhr = new XMLHttpRequest();
xhr.open('GET', "https://***.execute-api.***.amazonaws.com/dev/count", 
true);
xhr.send();
</script>
```
