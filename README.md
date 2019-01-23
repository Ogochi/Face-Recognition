# Face Recognition
Project done as a part of "High performance network services" class at University of Warsaw 2018/19.
## Description
Main part of the project was to create **Highly Available** and **easy to scale** service.

Project resulted in service consisiting of following parts:
- Frontend services - generating html files from templates
- Face recognition service - operations on images linked to face recognition
- Nginx front server - load balancing between front services and caching
- Mongo and MySQL databases - storing data
- RabbitMQ - offloading computations from frontend services to face recognition service

## Views and features
Main view - added images with lists of people on them
![Main view](https://i.imgur.com/uccqKEz.png)

People view - added people with their face pictures
![People view](https://i.imgur.com/ND0ESSD.png)

Single image view - fullsize image with marked faces
![Single image view](https://i.imgur.com/R6N2O80.png)

## Technology stack
- Frontend: **HTML/CSS**, **Bootstrap**, **Javascript**
- Backend: **Python**, **Flask**, **MongoDB**, **MySQL**, **Nginx**, **RabbitMQ**, **[face_recognition lib](https://github.com/ageitgey/face_recognition)**
- Other: **Docker**, **Git**

## How to run
After executing commands mentioned below whole service should be accessible on `localhost:8080`.

`docker-compose build;
docker-compose up`
