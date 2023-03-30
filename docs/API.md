# Website Crawler API Endpoint

This API endpoint provides a way to start, stop, and monitor website crawls, as well as initiate new crawls.

## Authentication

All requests to the API endpoint must include an API key in the header for authentication. The API key should be included in the `Authorization` header as a bearer token, like so:

`Authorization: Bearer <API_KEY>`

## Starting/Stopping a Crawl

To start a new crawl cycle, send a `POST` request to `localhost:8084/crawl/start`.

To stop an active crawl cycle, send a `POST` request to `localhost:8084/crawl/stop`.

Both requests should include an API key in the header for authentication.

## Monitoring Crawl Status

To check the status of active crawl cycles, send a `GET` request to `localhost:8084/crawl/status`. This request should include an API key in the header for authentication.

The response will be a JSON object containing information about active crawl cycles, like so:

```json
{
  "active_crawls": [
    {
      "url": "https://www.example.com",
      "status": "running",
      "progress": {
        "total_urls": 100,
        "crawled_urls": 50,
        "elapsed_time": "00:30:00"
      }
    },
    {
      "url": "https://www.anotherexample.com",
      "status": "stopped",
      "progress": {
        "total_urls": 200,
        "crawled_urls": 100,
        "elapsed_time": "01:00:00"
      }
    }
  ]
}
```

## Initiating a Crawl

To initiate a new crawl, send a `POST` request to `localhost:8084/crawl`. The request body should include the following information:

- "url": the URL of the website to crawl (required)
- "return_results": a boolean value indicating whether the results of the crawl should be returned to the requester (optional; defaults to false)
- "write_to_database": a boolean value indicating whether the results of the crawl should be written to the database (optional; defaults to true)

This request should include an API key in the header for authentication.

The response will be a JSON object containing information about the crawl, like so:

```json
{
  "id": "123456",
  "status": "running",
  "url": "https://www.example.com",
  "return_results": true,
  "write_to_database": true
}
```

If `return_results` is `true`, the response will include the results of the crawl as well.

If `write_to_database` is `true`, the results of the crawl will be written to the database.

```json
{
  "id": "123456",
  "status": "completed",
  "url": "https://www.example.com",
  "return_results": true,
  "write_to_database": true,
  "results": [
    {
      "url": "https://www.example.com/page1",
      "title": "Example Page 1"
    },
    {
      "url": "https://www.example.com/page2",
      "title": "Example Page 2"
    },
    {
      "url": "https://www.example.com/page3",
      "title": "Example Page 3"
    }
  ]
}
```

## Examples

Here are some example requests using `curl`:

Starting a crawl cycle:

```curl
curl -X POST
-H "Authorization: Bearer <
```
