# About Mayan automatic metadata

I wanted to be able to have my documents automatically tagged as I don't like to repeat these kinds of tasks over and over again.

This MAM *mayan automatic metadata* tool consists of three parts:

- The point where mayan does trigger some work.
- The worker, which does the processing
- The pluging *you* have to do on your own. Maybe I can share some at some point in time.

## HowTo

Assuming you already have mayan running in a docker environment. 
The docker-compose file should give you an example of how to get MAM up and running. If you run it standalone, you must have forward an external port to the port 3000 of the web part and you must add a reddis server.

The following environment variables are relevant:

- REDIS_URL: provide a proper redis url for the task queuing
- MAYAN_USER: a user which is allowed to access mayan, this user will read documents, add metadata and tags
- MAYAN_PASSWORD: for authentication a password for the user is required
- MAYAN_URL: The url to your mayan instance. Inlcude the /api/ at the end.

You may want to mount the plugin directory to the worker container.

More detailed example will follow.




