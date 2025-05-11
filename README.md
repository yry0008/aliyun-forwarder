# Aliyun Forwarder

A simple web server that forwards requests to Alibaba Cloud, avoid signature verification on the client side.

## Deployment

1. Automatically Deploy using Docker

```bash
docker run -d --name aliyun-forwarder -p 8000:8000 --restart always ghcr.io/yry0008/aliyun-forwarder:latest
```

2. Manually run the server

Ensure you have Python 3.8+ installed.
Clone the repository, install requirements and run the server using Python.

```bash
git clone https://github.com/yry0008/aliyun-forwarder.git
cd aliyun-forwarder
pip install -r requirements.txt
python3 -m main.py
```

## Usage

We add some headers to the request, here are the headers we add:

| Header | Description | Example |
|--------|-------------|---------|
| access-key | Your Alibaba Cloud Access Key ID | ak |
| secret-key | Your Alibaba Cloud Access Key Secret | sk |
| endpoint | The endpoint of the service you want to access | business.aliyuncs.com |
| action | The action you want to perform | QueryAccountBalance |
| version | The version of the API you want to use | 2017-12-14 |

Here is an simple example of how to use the forwarder:

```bash
curl -X 'GET' \
  'http://localhost:8000/' \
  -H 'accept: application/json' \
  -H 'access-key: ak' \
  -H 'secret-key: sk' \
  -H 'endpoint: business.aliyuncs.com' \
  -H 'action: QueryAccountBalance' \
  -H 'version: 2017-12-14'
```
The above command will forward the request to the Alibaba Cloud API and return the response.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
