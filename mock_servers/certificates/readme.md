# To generate ssl cert + key

```
openssl req -config knnect.conf -new -x509 -sha256 -newkey rsa:2048 -nodes -keyout example-com.key.pem -days 2365 -out example-com.cert.pem
```