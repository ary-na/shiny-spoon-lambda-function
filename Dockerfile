FROM scratch
ADD x86_64/08aa155acd260bd38998478bb10994c34e8244a70d6a8ed3db6cc2fb691c06f5.tar.xz /
ADD x86_64/24714ddfb358f9175cccbe5de6d57886c4742daa08bfb8fba4f66da0b7c3c666.tar.xz /
ADD x86_64/29c2afcfa1be1df0fda2a12433298a3f8b4c5ae16e4ca29ddc7924d84b4df49d.tar.xz /
ADD x86_64/39be15d98d5fe1f524b394e1e662cc2b38ff4e0c2b5ebe5d3dc3aaacffd0a732.tar.xz /
ADD x86_64/e9991bdacaf94ad1450685b3a58997d86576dbcef3b7dccc852009f432fb8624.tar.xz /
ADD x86_64/fa13b472ae60f71418c7d4421b0c194d8a82bb6c8808b021d8bbff254f936dd7.tar.xz /

ENV LANG=en_US.UTF-8
ENV TZ=:/etc/localtime
ENV PATH=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin
ENV LD_LIBRARY_PATH=/var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib
ENV LAMBDA_TASK_ROOT=/var/task
ENV LAMBDA_RUNTIME_DIR=/var/runtime

WORKDIR /var/task

ENTRYPOINT ["/lambda-entrypoint.sh"]