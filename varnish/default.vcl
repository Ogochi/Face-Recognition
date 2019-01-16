vcl 4.0;

backend default {
    .host = "nginx";
    .port = "8080";
}

sub vcl_backend_response {
    set beresp.ttl = 2s;
}
