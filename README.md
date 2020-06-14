# numberClassifier 

  

I have divided the project into three different directories `trainer`, `server`, and `client`. Bellow I will go into further details on how use each section and some thoughts about them. 

  

## Trainer. 

  

### Quick Start 

First move down to the correct directory: 

``` 

cd trainer 

``` 

  

Then build the default image, in this case we can label it `trainer`: 

``` 

docker build -t trainer . 

``` 

  

To run the container, I recommend the following command, where `EPOCHS` is the number of epochs to run, and the container will output a .h5 model to the current directory. 

``` 

docker run -it --rm -e EPOCHS="5" -v $(pwd):/tmp/numberClassifier/output trainer 

``` 

### Comments 

This model was heavily influenced by https://www.tensorflow.org/tutorials/quickstart/beginner  

  

## Server. 

### Quick Start 

First move down to the correct directory: 

``` 

cd server 

``` 

Copy the model file to this directory as such: 

``` 

cp ../trainer/numberClassifier.h5 . 

``` 

To build the server container simply 

``` 

docker build -t server . 

``` 

To run the container on the local machine I recommend the following command: 

``` 

docker run -it --rm -p 8085:8085 server 

``` 

or 

``` 

docker run -it --rm --net="host" server 

``` 

  

Allow a few seconds for all the services to start. 

### Comments 

Once the container is running there should be information on the terminal about the loaded TF models and the NGINX workers. 

  

Because we used connexion we now have a new swagger UI for our API at: http://localhost:8085/v1/ui/#/ 

  

The main point of interaction with the API is the `/v1/inference` endpoint which can receive `GET` and `POST` requests. For more information refer to the swagger UI or the client code. 

  

Lastly this is a multi-threaded implementation for the server, this should allow us to service requests more efficiently and faster. However, TF does not handle the multi-threaded nature of this environment (https://github.com/tensorflow/tensorflow/issues/8220) so, we have made some modifications to it to keep the performance benefits. We allow a 'lazy-app' approach from uwsgi that will load a TF model per thread. This is obviously wasteful and memory intensive, but for such a small model and I think it is ok for the performance benefits. 

The next design decision was to merge the inference layer and the REST API layer into one, even in a single python file. This is in my opinion un-ideal but for simplicity sake I think it should be ok in this example. 

  

Which brings me to redis, if we wanted to solve both these issues, I would recommend an in-memory message passer like redis. Through redis we could have a single "inference layer" then talk to the API layer, I have included Redis in this example as a super quick cheap database to keep previous classification results for now, but I think it can easily be expanded to solve the outlined issues. 

  

## Client 

### Quick Start 

The CLI client is simply called client.py, to run this utility you will need python3, and requests. 

  

  

To display a small help menu: `python3 client.py -h` 

  

The program has two modes `list` and `send`. Both modes can take a `--host` and `--port` flag to set the location of the server, they currently default to localhost and 8085 

  

`list` takes no further arguments and display all previous inference results. 

  

`send` takes a file path with `--filepath` for the location of the file to classify and displays the result of this classification. 

  

There is a small simple website to interact with the service at `simple-site.html` to visit simply navigate to that file on your browser, for me that is `file:///home/jpvillam/numberClassifier/client/simple-site.html` 

The website should allow you to upload files and see previous results. Something very simple but another way to interact with the service.  

  

### Comments 

  

Ideally the website should be hosted with the server to not have CORS, but in an effort to keep them separate I decided to not host it and just have it local. 

 
