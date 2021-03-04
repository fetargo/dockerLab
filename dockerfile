FROM amazonlinux
LABEL version=1.0
LABEL description=Yashin_A.A._727-1_Lab1-Docker
COPY legShot.sh .
RUN chmod ugo+x legShot.sh
RUN yum -y install openldap-devel
RUN useradd -p 1111 user1
CMD ./legShot.sh
