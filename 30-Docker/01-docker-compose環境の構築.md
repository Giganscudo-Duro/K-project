# docker-compose $B$N%$%s%9%H!<%k(B
docker-compose $B$K$O@lMQ$N%Q%C%1!<%8$J$I$OL5$$$N$G!"<B9T%U%!%$%k$r%@%&%s%m!<%I!u<B9T8"8BIUM?$H$$$&A`:n$K$J$k!#(B
$B@h$:$O>e5-$r<B9T$9$k$?$a!"0J2<$N%3%^%s%I$r<B9T$9$k!#(B
```shell
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.28.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```
$B<B9T8"8B$rIUM?$G$-$J$$$H$-$O!"0J2<$N%3%^%s%I$GBeMQ$9$k!#(B
```shell
$ sudo chmod 755 /usr/local/bin/docker-compose
```

# docker-compose $B$N%"%C%W%0%l!<%I(B
docker-compose $B$O<B9T%U%!%$%k$r%@%&%s%m!<%I$7$F;H$&$H$$$&@-<A>e!"(B`yum` $B%3%^%s%I$G%"%C%W%0%l!<%I=PMhL5$$!#(B
$B$=$N$?$a!"0J2<$N%3%^%s%I$r<B9T$7$F!"%"%C%W%0%l!<%I$r9T$&$3$H$K$J$k!#(B
$B$?$@!"(B`--help` $B8+$F$b!"$=$s$J%*%W%7%g%s$J$$$s$@$h$J$!!#(B
```shell
$ sudo docker-compose migrate-to-labels
```

# docker-compose $B$N%"%s%$%s%9%H!<%k(B
docker-compose $B$r%"%s%$%s%9%H!<%k$7$?$$>l9g$O!"(Bdocker-compose $B$N<B9T%U%!%$%k$r:o=|$9$l$P(BOK$B!#(B
$B0J2<$N%3%^%s%I$r<B9T$9$k!#(B
```shell
$ sudo rm /usr/local/bin/docker-compose
```


# $B;29M(BURL

- [Install Docker Compose - Docker Docs](https://docs.docker.com/compose/install/)
