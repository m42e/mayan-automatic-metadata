# About Mayan automatic metadata

> [!WARNING]  
> This is currently unmaintained, as my use-case is done and I see this as a proof of concept.
> Feel free to contact me if you like to maintain it.

I wanted to be able to have my documents automatically tagged as I don't like to repeat these kinds of tasks over and over again.

This MAM *mayan automatic metadata* tool consists of three parts:

- The point where mayan does trigger some work.
- The worker, which does the processing
- The pluging *you* have to do on your own. Maybe I can share some at some point in time.

## HowTo

The prequesites you have to have:

- Running mayan, accessible from the node you run this on, and vice versa (for the webhook)
- A user in mayan, which is allowed to access the documents and the documents parsed content as well as the OCR content.
- docker (You may be able to do it outside of docker, but I don't care)

You could either let MAM have its own docker stack (including network) then you have to publish some ports. Or the prefered way, having it in the same network which is what is described here.

Add the contents of the docker-compose file to the one you are using for mayan already.

```
version: '2'

services:
  mayan-mam-web:
    container_name: mayan-mam-web
    image: m42e/mayan-mam-web
    restart: always
    environment:
      REDIS_URL: redis://results:6379/
      
  mayan-mam-worker:
    container_name: mayan-mam-worker
    image: m42e/mayan-mam-worker
    restart: always
    environment:
      REDIS_URL: redis://results:6379/
      MAYAN_USER: mam-user
      MAYAN_PASSWORD: secretpassword
      MAYAN_URL: https://yourinstance/api/
      USE_GIT_PLUGINS: 0
      GIT_PLUGINS_URL: https://mygithubuser:<applicationtoken>@github.com/mygithubuser/mam-plugins

```

We are having twos services here, one is the *webfrontend* (hilarious to call it so, as it only creates tasks for the worker, no real frontend).
This offers and endpoint to use in mayan workflows. The endpoint is located at the base url, so from inside the stack: `http://mayam-mam-web:8000/`.

The following environment variables are relevant:

- `REDIS_URL`: provide a proper redis url for the task queuing
- `MAYAN_USER`: a user which is allowed to access mayan, this user will read documents, add metadata and tags
- `MAYAN_PASSWORD`: for authentication a password for the user is required
- `MAYAN_URL`: The url to your mayan instance. Inlcude the /api/ at the end.
- `GIT_PLUGINS_URL`: The url, including a possibly required authentication, to the git repository containing your plugin. (Example: <https://github.com/m42e/mayan-automatic-metadata-plugins>)
- `USE_GIT_PLUGINS`: If set to 1 the plugin directory will be cleared and the plugins of the git repository specified will be used.

You could also mount (with docker) the `/app/plugins` directory to a folder of your choice, where you place the plugins.


# Trigger it

The way of triggering is quite simple. Just drop a `POST` or `GET` request to the endpoint with the documentid attached. E. g. `http://mayan-mam-web:8000/345`
This will enqueue the task for the worker.

*NB*: This should be done after the OCR content is available.

# The workers job

The worker receiving the processing request, will get the required information from mayan, read the documents data and applies its strategies to get the values and add tags.

That's all folks.




