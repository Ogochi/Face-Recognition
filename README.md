# JNP3
# How to run
# Let's create our internal network
`docker network create jnp3_network`

# We need to create mongo first, becoase flask uses it
`docker run --net jnp3_network --name jnp3_mongo -d mongo`

# We need to run rabbitmq next
#OLD`docker run --net jnp3_network -e RABBITMQ_PASSWORD=2137 --name rabbit bitnami/rabbitmq:latest`
`docker run --net jnp3_network -e RABBITMQ_DEFAULT_PASS=2137  -e RABBITMQ_DEFAULT_USER=user --name rabbit rabbitmq:latest`
# Go to flask directory and then ( better to run it in second terminal to see logs )
`docker-compose build
docker-compose up`

# Now check your localhost:{5000-5002}, and submit few request
# There should be same list in all three hosts - same mongodb

# Now lets get our loadbalancer works
# Go to nginx dir and
`docker build . -t jnp3_nginx_image`

# And lets runit in our network (pplease mind that i randomly chosed port 3333 )
`docker run -p 3333:8080 --net jnp3_network -d --name jnp3_nginx jnp3_nginx_image`

# Check your localhost:3333 and refresh few times
# Look at flask logs

# Run main docker-compose
`docker-compose build
docker-compose up`
